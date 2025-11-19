
import sys
from pathlib import Path

try:
    import werkzeug  # type: ignore
    if not hasattr(werkzeug, "__version__"):
        # Provide a fallback version string used for tests only
        werkzeug.__version__ = "3.1.3"
except Exception:
    # If werkzeug import fails, tests will later fail more explicitly. We don't crash here.
    pass


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
