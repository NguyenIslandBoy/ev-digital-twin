# policy/environment.py
"""
Gymnasium environment wrapping the Mesa ChargingNetworkModel for RL pricing.

One episode = one simulated day (48 x 30-min steps). Each step the agent sets a
network-wide price level; the model advances 30 minutes; the agent receives an
incremental revenue-vs-wait reward.

Design decisions (see project plan):
  - Regime          : high-adoption (2x) — the only regime with a real trade-off
  - Action space    : Discrete(3) -> {£0.15, £0.30, £0.45} network-wide
  - Demand response : price_elasticity>0 enables abandonment (the downside to
                      high prices). Passed straight to the model so an
                      elasticity sensitivity sweep is a one-line change.
  - Reward          : per-step, incremental, dense:
                        reward = d_revenue - lambda_wait * d_wait_steps
                                            - lambda_co2  * d_co2/1000
                      lambda_co2 defaults to 0 (CO2 excluded from the first
                      working agent; hourly_carbon flag left available for the
                      stretch objective).
"""

from __future__ import annotations

import numpy as np
import gymnasium as gym
from gymnasium import spaces

from simulation.model import ChargingNetworkModel
from simulation.config import STEPS_PER_DAY, N_CHARGERS


# Discrete price menu (£/kWh). Index = action.
PRICE_LEVELS = np.array([0.15, 0.30, 0.45], dtype=np.float32)
_PRICE_MAX = float(PRICE_LEVELS.max())


class ChargingPricingEnv(gym.Env):
    """RL environment for network-wide EV charging price control."""

    metadata = {"render_modes": []}

    def __init__(
        self,
        adoption_multiplier: float = 2.0,
        price_elasticity:    float = 0.8,
        lambda_wait:         float = 0.75,  # ~tie-point between the two price
                                            # constants; recalibrate per regime
                                            # with signal_check.py on real data
        lambda_co2:          float = 0.0,
        hourly_carbon:       bool  = False,
        queue_norm:          float = 15.0,   # queue length that maps to obs=1.0
        seed:                int | None = None,
    ):
        super().__init__()
        self.adoption_multiplier = adoption_multiplier
        self.price_elasticity    = price_elasticity
        self.lambda_wait         = lambda_wait
        self.lambda_co2          = lambda_co2
        self.hourly_carbon       = hourly_carbon
        self.queue_norm          = queue_norm

        self.n_chargers    = int(N_CHARGERS)
        self.steps_per_day = int(STEPS_PER_DAY)

        # Action: choose one of the 3 price levels
        self.action_space = spaces.Discrete(len(PRICE_LEVELS))

        # Observation (all scaled into [0, 1]):
        #   step_frac(1) | occupancy(n) | queue_norm(n) | price_norm(1) | arrivals_frac(1)
        obs_dim = 1 + self.n_chargers + self.n_chargers + 1 + 1
        self.observation_space = spaces.Box(
            low=0.0, high=1.0, shape=(obs_dim,), dtype=np.float32
        )

        self._model: ChargingNetworkModel | None = None
        self._prev_rev = 0.0
        self._prev_wait = 0.0
        self._prev_co2 = 0.0

    # ── model construction ────────────────────────────────────────────────────
    def _build_model(self, seed: int) -> ChargingNetworkModel:
        return ChargingNetworkModel(
            seed=seed,
            adoption_multiplier=self.adoption_multiplier,
            price_per_kwh=0.30,                # neutral starting price
            price_elasticity=self.price_elasticity,
            hourly_carbon=self.hourly_carbon,
        )

    # ── observation & snapshots ───────────────────────────────────────────────
    def _get_obs(self) -> np.ndarray:
        m = self._model
        occ = [1.0 if c.is_occupied else 0.0 for c in m.charger_agents]
        que = [min(len(c.queue) / self.queue_norm, 1.0) for c in m.charger_agents]
        step_frac = m.current_step / self.steps_per_day
        price_norm = m.price_per_kwh / _PRICE_MAX
        arrivals_frac = (
            m._arrivals_remaining / m.daily_session_target
            if m.daily_session_target > 0 else 0.0
        )
        obs = np.array(
            [step_frac, *occ, *que, price_norm, arrivals_frac],
            dtype=np.float32,
        )
        # guard against any float drift outside the declared box
        return np.clip(obs, 0.0, 1.0)

    def _snapshot(self) -> tuple[float, float, float]:
        m = self._model
        rev  = sum(c.total_revenue     for c in m.charger_agents)
        wait = sum(c.total_wait_steps  for c in m.charger_agents)
        co2  = sum(c.total_co2_g       for c in m.charger_agents)
        return rev, wait, co2

    # ── Gymnasium API ─────────────────────────────────────────────────────────
    def reset(self, *, seed: int | None = None, options: dict | None = None):
        super().reset(seed=seed)
        # Draw a fresh per-episode model seed from the env RNG so training sees
        # varied days but runs are reproducible given the env seed.
        model_seed = int(self.np_random.integers(0, 2**31 - 1))
        self._model = self._build_model(model_seed)
        self._prev_rev, self._prev_wait, self._prev_co2 = self._snapshot()
        return self._get_obs(), {}

    def step(self, action):
        m = self._model
        price = float(PRICE_LEVELS[int(action)])
        m.price_per_kwh = price          # agents this step see this price

        m.step()

        rev, wait, co2 = self._snapshot()
        d_rev  = rev  - self._prev_rev
        d_wait = wait - self._prev_wait
        d_co2  = co2  - self._prev_co2
        self._prev_rev, self._prev_wait, self._prev_co2 = rev, wait, co2

        reward = (
            d_rev
            - self.lambda_wait * d_wait
            - self.lambda_co2 * (d_co2 / 1000.0)
        )

        terminated = False                       # no failure state
        truncated  = m.current_step >= self.steps_per_day   # day complete

        info = {
            "price":          price,
            "d_revenue":      d_rev,
            "d_wait_steps":   d_wait,
            "cum_revenue":    rev,
            "cum_wait_steps": wait,
        }
        return self._get_obs(), float(reward), terminated, truncated, info

    def render(self):
        return None

    def close(self):
        self._model = None


def make_env(**kwargs):
    """Factory for SB3 (e.g. make_vec_env(make_env, n_envs=8))."""
    def _thunk():
        return ChargingPricingEnv(**kwargs)
    return _thunk