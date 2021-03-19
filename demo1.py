from core.universe.pyportframe import PyPort
from core.settings import EXAMPLES_DIR

p = PyPort('silly', EXAMPLES_DIR)

print(p.instructions)
print(p.declared_assets)
print(p.portfolios)

print(p.cumulative_returns)