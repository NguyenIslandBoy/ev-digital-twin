# simulation/agents.py

import numpy as np
from mesa import Agent

from simulation.config import (
    CONNECTOR_SHARES,
    CONNECTOR_ENERGY,
    CONNECTOR_DURATION,
    MAX_DURATION_HRS,
    MIN_ENERGY_KWH,
    STEP_MINUTES,
    PRICE_PER_KWH,
    CARBON_PENALTY,
)


# ── HELPER: sample connector type ─────────────────────────────────────────────
def _sample_connector(rng: np.random.Generator) -> str:
    connectors = list(CONNECTOR_SHARES.keys())
    shares     = list(CONNECTOR_SHARES.values())
    return rng.choice(connectors, p=shares)


# ── HELPER: sample energy demand (empirical) ──────────────────────────────────
def _sample_energy(connector: str, rng: np.random.Generator) -> float:
    values = CONNECTOR_ENERGY[connector]["values"]
    energy = rng.choice(values)
    return max(MIN_ENERGY_KWH, float(energy))


# ── HELPER: sample session duration (Gamma) ───────────────────────────────────
def _sample_duration(connector: str, rng: np.random.Generator) -> float:
    from scipy.stats import lognorm
    p = CONNECTOR_DURATION[connector]
    duration = lognorm.rvs(
        s=p["s"], loc=p["loc"], scale=p["scale"],
        random_state=rng
    )
    return float(np.clip(duration, 0.1, MAX_DURATION_HRS))


# ─────────────────────────────────────────────────────────────────────────────
class ChargerAgent(Agent):
    """
    Represents a physical EV charger (one connector slot).
    Tracks occupancy, queue, and accumulated metrics per episode.
    """

    def __init__(self, unique_id: int, model):
        super().__init__(unique_id, model)
        self.charger_id:    int   = unique_id
        self.is_occupied:   bool  = False
        self.current_ev:    "EVDriverAgent | None" = None
        self.queue:         list  = []           # waiting EVDriverAgents

        # Episode-level metrics
        self.total_sessions:     int   = 0
        self.total_energy_kwh:   float = 0.0
        self.total_revenue:      float = 0.0
        self.total_co2_g:        float = 0.0
        self.total_wait_steps:   int   = 0       # sum of queue wait steps
        self.utilisation_steps:  int   = 0       # steps charger was occupied

    def request_charge(self, ev: "EVDriverAgent") -> bool:
        """
        EV requests to charge. Returns True if charging starts immediately,
        False if added to queue.
        """
        if not self.is_occupied:
            self._start_charging(ev)
            return True
        else:
            self.queue.append(ev)
            return False

    def _start_charging(self, ev: "EVDriverAgent") -> None:
        self.is_occupied  = True
        self.current_ev   = ev
        ev.is_charging    = True
        ev.charger        = self
        ev.wait_steps     = 0

    def step(self) -> None:
        """Advance charger by one time step."""
        if self.is_occupied and self.current_ev is not None:
            self.utilisation_steps += 1
            ev = self.current_ev

            # Charge the EV for one step
            charge_this_step = min(
                ev.charge_rate_kwh_per_step,
                ev.energy_remaining_kwh
            )
            ev.energy_remaining_kwh -= charge_this_step

            # Accumulate metrics
            carbon_intensity = self.model.carbon_intensity_g_per_kwh
            self.total_energy_kwh += charge_this_step
            self.total_revenue    += charge_this_step * self.model.price_per_kwh
            self.total_co2_g      += charge_this_step * carbon_intensity

            # Check if session complete
            ev.steps_remaining -= 1
            if ev.energy_remaining_kwh <= 0.01 or ev.steps_remaining <= 0:
                self._end_session(ev)

        # Increment wait steps for queued EVs
        for queued_ev in self.queue:
            queued_ev.wait_steps    += 1
            self.total_wait_steps   += 1

    def _end_session(self, ev: "EVDriverAgent") -> None:
        """Session complete — release charger and serve next in queue."""
        self.total_sessions  += 1
        self.is_occupied      = False
        self.current_ev       = None
        ev.is_charging        = False
        ev.session_complete   = True
        self.model.completed_sessions += 1

        # Serve next in queue if any
        if self.queue:
            next_ev = self.queue.pop(0)
            self._start_charging(next_ev)

    @property
    def utilisation_rate(self) -> float:
        total = self.model.current_step
        return self.utilisation_steps / total if total > 0 else 0.0

    @property
    def avg_wait_steps(self) -> float:
        return (
            self.total_wait_steps / self.total_sessions
            if self.total_sessions > 0 else 0.0
        )


# ─────────────────────────────────────────────────────────────────────────────
class EVDriverAgent(Agent):
    """
    Represents an EV driver arriving to charge.
    Samples connector type, energy demand, and session duration from
    calibrated empirical distributions.
    """

    def __init__(self, unique_id: int, model):
        super().__init__(unique_id, model)
        rng = model.rng

        # Sample characteristics from calibrated distributions
        self.connector_type:        str   = _sample_connector(rng)
        self.energy_demand_kwh:     float = _sample_energy(self.connector_type, rng)
        self.energy_remaining_kwh:  float = self.energy_demand_kwh
        self.duration_hrs:          float = _sample_duration(self.connector_type, rng)

        # Charging rate derived from energy and duration
        # kWh per 30-min step
        self.charge_rate_kwh_per_step: float = (
            self.energy_demand_kwh / max(self.duration_hrs * 2, 1)
        )

        # Steps required to complete session
        self.steps_remaining: int = max(
            1, int(self.duration_hrs * (60 / STEP_MINUTES))
        )

        # State
        self.is_charging:     bool  = False
        self.session_complete: bool = False
        self.charger:         "ChargerAgent | None" = None
        self.wait_steps:      int   = 0
        self.assigned:        bool  = False

    def step(self) -> None:
        """
        If not yet assigned to a charger, attempt to find one.
        Charging progression is handled by ChargerAgent.step().
        """
        if self.session_complete or self.is_charging:
            return

        if not self.assigned:
            self._find_charger()

    def _find_charger(self) -> None:
        """
        Select charger with shortest queue (greedy strategy).
        In Phase 4, this will be replaced by the RL policy.
        """
        chargers = self.model.charger_agents
        # Pick charger with shortest queue
        target = min(
            chargers,
            key=lambda c: len(c.queue) + (1 if c.is_occupied else 0)
        )
        target.request_charge(self)
        self.assigned = True