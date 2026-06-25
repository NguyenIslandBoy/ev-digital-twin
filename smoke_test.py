from simulation.model import ChargingNetworkModel
import numpy as np

# Run 100 episodes and check session count distribution
session_counts = []
for i in range(500):
    model = ChargingNetworkModel(seed=i, is_weekday=True)
    kpis  = model.run_episode()
    session_counts.append(kpis["sessions_completed"])

print(f"Mean : {np.mean(session_counts):.2f}  (real: 25.11)")
print(f"Std  : {np.std(session_counts):.2f}  (real: 10.38)")
print(f"Min  : {np.min(session_counts)}  (real: 3)")
print(f"Max  : {np.max(session_counts)}  (real: 59)")