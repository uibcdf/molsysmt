from argdigest import arg_digest
from argdigest.core.config import DigestConfig
import sys

# Explict config
cfg = DigestConfig(digestion_style="decorator", strictness="ignore")

@arg_digest.map(a={'kind':'std','rules':['to_bool']}, config=cfg)
def f(a):
    return a

try:
    print("Calling f('yes')...")
    res = f('yes')
    print("Result:", res)
except ZeroDivisionError:
    print("SUCCESS: ZeroDivisionError caught!")
except Exception as e:
    print(f"Caught other error: {type(e).__name__}: {e}")