"""Linux-first citizen services OS learning platform.

The Phase 1 and Phase 2 source trees intentionally share the citizen_os
namespace. Extend the package path so both sets of modules remain importable.
"""
from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)
__version__ = "0.1.0"
