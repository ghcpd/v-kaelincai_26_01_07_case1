import sys
from pathlib import Path

# Ensure project root is on sys.path so tests can import package modules
ROOT = Path(__file__).parent.parent.resolve()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
