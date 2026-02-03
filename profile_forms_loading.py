import cProfile
import pstats
from molsysmt.form import _dict_modules
import time

print("Starting profiling of forms loading...")
start = time.time()

def load_all():
    # Force loading of everything
    _dict_modules.clear()
    _dict_modules._initialized = False
    _dict_modules._ensure_initialized()

# Profile it
profiler = cProfile.Profile()
profiler.enable()
try:
    load_all()
finally:
    profiler.disable()

end = time.time()
print(f"Total time: {end - start:.4f} seconds")

# Stats
stats = pstats.Stats(profiler).sort_stats('cumtime')
stats.print_stats(30)
