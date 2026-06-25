from simulation.model import ChargingNetworkModel
import numpy as np

# Run 100 episodes and check session count distribution
session_counts = []
for i in range(100):
    model = ChargingNetworkModel(seed=i, is_weekday=True)
    kpis  = model.run_episode()
    session_counts.append(kpis["sessions_completed"])

print(f"Mean sessions/day : {np.mean(session_counts):.2f}")
print(f"Std               : {np.std(session_counts):.2f}")
print(f"Min               : {np.min(session_counts)}")
print(f"Max               : {np.max(session_counts)}")
print(f"Real mean         : 24.81")