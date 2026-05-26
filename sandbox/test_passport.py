import time
import numpy as np
from molsysmt import pyunitwizard as puw
from molsysmt.structure import get_contacts
from argdigest.core.contract import ValidatedPayload
import molsysmt as msm

# Load a real molecular system
print("Loading Trp-cage (1l2y) system...")
molsys = msm.convert("1l2y")

# Get coordinates
coords = msm.get(molsys, element="atom", selection="all", coordinates=True)
print("Coordinates shape:", coords.shape)
print("Coordinates type:", type(coords))

# 1. Warm-up
print("\nWarming up...")
for _ in range(5):
    _ = get_contacts(molsys, selection="atom_name == 'CA'", threshold="12 angstroms")

# 2. Benchmark WITHOUT Passport
print("\nRunning benchmark WITHOUT Passport (Normal validation)...")
t0 = time.perf_counter()
for _ in range(100):
    _ = get_contacts(molsys, selection="atom_name == 'CA'", threshold="12 angstroms")
t1 = time.perf_counter()
time_normal = (t1 - t0) * 1000.0
print(f"Time for 100 iterations (Normal): {time_normal:.2f} ms ({time_normal/100:.3f} ms/iter)")

# Let's see: how can we pass a ValidatedPayload?
# In get_contacts, the arguments that get digested include 'selection' and 'threshold'.
# 'threshold' is digested using digest_threshold in threshold.py.
# Let's create a ValidatedPayload for 'threshold'!
threshold_qty = puw.quantity(1.2, "nm")
payload_threshold = ValidatedPayload(value=threshold_qty, unit="nm", dtype="float64")

# 3. Benchmark WITH Passport for threshold
print("\nRunning benchmark WITH Passport for threshold...")
# Let's warm up
for _ in range(5):
    _ = get_contacts(molsys, selection="atom_name == 'CA'", threshold=payload_threshold)

t0 = time.perf_counter()
for _ in range(100):
    _ = get_contacts(molsys, selection="atom_name == 'CA'", threshold=payload_threshold)
t1 = time.perf_counter()
time_passport = (t1 - t0) * 1000.0
print(f"Time for 100 iterations (Passport): {time_passport:.2f} ms ({time_passport/100:.3f} ms/iter)")
print(f"Speedup: {time_normal / time_passport:.2f}x")
