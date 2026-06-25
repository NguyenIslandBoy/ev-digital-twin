# simulation/model.py

import numpy as np
from mesa import Model
from mesa.time import RandomActivation

from simulation.agents import EVDriverAgent, ChargerAgent
from simulation.config import (
    CHARGER_IDS,
    N_CHARGERS,
    ARRIVAL_RATES,
    STEPS_PER_DAY,
    RANDOM_SEED,
    WEEKDAY_RATIO,
    PRICE_PER_KWH,
    CARBON_PENALTY,
    ADOPTION_MULTIPLIER,
    NB_R,
    NB_P,
)


class ChargingNetworkModel(Model):
    """
    Agent-based digital twin of the USB EV charging network.

    One episode = one simulated day (48 steps of 30 minutes each).
    At each step:
      1. New EV agents arrive (Poisson-sampled from calibrated arrival rates)
      2. EVDriverAgents attempt to find a charger
      3. ChargerAgents process charging and update queues

    KPIs tracked per episode:
      - Total sessions completed
      - Total energy delivered (kWh)
      - Total revenue (£)
      - Total CO2 emissions (gCO2)
      - Average waiting time (steps)
      - Per-charger utilisation rate
    """

    def __init__(
        self,
        seed:                int   = RANDOM_SEED,
        is_weekday:          bool  = True,
        price_per_kwh:       float = PRICE_PER_KWH,
        carbon_penalty:      float = CARBON_PENALTY,
        adoption_multiplier: float = ADOPTION_MULTIPLIER,
        carbon_intensity:    float = 60.0,    # gCO2/kWh (mean from EDA)
    ):
        super().__init__()
        self.rng = np.random.default_rng(seed)

        # Scenario parameters — overridden by scenario engine
        self.is_weekday          = is_weekday
        self.price_per_kwh       = price_per_kwh
        self.carbon_penalty      = carbon_penalty
        self.adoption_multiplier = adoption_multiplier
        self.carbon_intensity_g_per_kwh = carbon_intensity

        # Scheduler — chargers step before EV agents
        self.schedule = RandomActivation(self)

        # Time tracking
        self.current_step = 0

        # Episode-level counters
        self.completed_sessions = 0
        self.ev_agent_counter   = 0    # unique ID counter for EV agents

        # ── Create charger agents ─────────────────────────────────────────────
        self.charger_agents: list[ChargerAgent] = []
        for charger_id in CHARGER_IDS:
            charger = ChargerAgent(charger_id, self)
            self.charger_agents.append(charger)
            self.schedule.add(charger)
            
        self.daily_session_target: int = int(
        self.rng.negative_binomial(n=NB_R, p=NB_P)
        )
        self._arrivals_remaining: int = self.daily_session_target    

    # ── ARRIVAL LOGIC ─────────────────────────────────────────────────────────
    def _get_arrival_rate(self) -> float:
        hour = (self.current_step * 30) // 60
        base_rate = ARRIVAL_RATES.get(hour, 0.0)
        return base_rate * self.adoption_multiplier

    def _spawn_arrivals(self) -> None:
        """
        Distribute daily session target across steps proportionally
        to the empirical hourly arrival rates.
        """
        if self._arrivals_remaining <= 0:
            return

        rate     = self._get_arrival_rate()
        total    = sum(ARRIVAL_RATES.values())
        fraction = rate / total if total > 0 else 0.0

        # Expected arrivals this step from daily target
        expected  = fraction * self.daily_session_target
        n_arrive  = min(
            self._arrivals_remaining,
            int(self.rng.poisson(lam=max(expected, 0)))
        )
        self._arrivals_remaining -= n_arrive

        for _ in range(n_arrive):
            self.ev_agent_counter += 1
            ev = EVDriverAgent(
                unique_id=self.ev_agent_counter,
                model=self
            )
            self.schedule.add(ev)

    # ── STEP ─────────────────────────────────────────────────────────────────
    def step(self) -> None:
        """Advance simulation by one 30-minute step."""
        self._spawn_arrivals()
        self.schedule.step()
        self.current_step += 1

    # ── RUN FULL EPISODE ─────────────────────────────────────────────────────
    def run_episode(self) -> dict:
        """
        Run a full day (48 steps) and return KPI summary.
        Used for calibration validation and scenario evaluation.
        """
        for _ in range(STEPS_PER_DAY):
            self.step()
        return self.get_kpis()

    # ── KPIs ─────────────────────────────────────────────────────────────────
    def get_kpis(self) -> dict:
        """Aggregate KPIs across all chargers for this episode."""
        total_energy    = sum(c.total_energy_kwh   for c in self.charger_agents)
        total_revenue   = sum(c.total_revenue       for c in self.charger_agents)
        total_co2       = sum(c.total_co2_g         for c in self.charger_agents)
        total_sessions  = sum(c.total_sessions      for c in self.charger_agents)
        total_wait      = sum(c.total_wait_steps    for c in self.charger_agents)

        avg_utilisation = np.mean([
            c.utilisation_rate for c in self.charger_agents
        ])

        avg_wait_steps  = (
            total_wait / total_sessions if total_sessions > 0 else 0.0
        )
        avg_wait_hrs    = avg_wait_steps * 0.5    # steps to hours

        # Queue length at end of episode
        total_queued = sum(len(c.queue) for c in self.charger_agents)

        return {
            "sessions_completed":   total_sessions,
            "energy_kwh":           round(total_energy,   2),
            "revenue_gbp":          round(total_revenue,  2),
            "co2_g":                round(total_co2,      2),
            "avg_wait_hrs":         round(avg_wait_hrs,   3),
            "avg_utilisation":      round(avg_utilisation, 4),
            "sessions_queued_end":  total_queued,
            "ev_agents_spawned":    self.ev_agent_counter,
        }

    # ── RESET ─────────────────────────────────────────────────────────────────
    def reset(self, seed: int | None = None) -> None:
        """
        Reset model for a new episode without reinitialising chargers.
        Used by the Gym environment wrapper in Phase 4.
        """
        if seed is not None:
            self.rng = np.random.default_rng(seed)

        self.current_step       = 0
        self.completed_sessions = 0
        self.ev_agent_counter   = 0

        self.daily_session_target = int(
        self.rng.negative_binomial(n=NB_R, p=NB_P)
        )
        self._arrivals_remaining = self.daily_session_target
        
        # Clear charger state
        for charger in self.charger_agents:
            charger.is_occupied       = False
            charger.current_ev        = None
            charger.queue             = []
            charger.total_sessions    = 0
            charger.total_energy_kwh  = 0.0
            charger.total_revenue     = 0.0
            charger.total_co2_g       = 0.0
            charger.total_wait_steps  = 0
            charger.utilisation_steps = 0

        # Remove all EV agents from scheduler
        ev_agents = [
            a for a in self.schedule.agents
            if isinstance(a, EVDriverAgent)
        ]
        for ev in ev_agents:
            self.schedule.remove(ev)