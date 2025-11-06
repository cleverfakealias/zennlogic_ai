"""Compatibility shim package.

Expose the existing `service` package under the historical
`zennlogic_ai_service` package name so tests and external code that import
`zennlogic_ai_service.*` continue to work after we refactored internal
imports to `service.*`.

This sets the package __path__ to the underlying `service` package path so
that subpackage imports like `zennlogic_ai_service.rest` resolve correctly.
"""

from importlib import import_module
import warnings


# Import the actual package and adopt its path so this package becomes an
# alias for `service` at import time.
_service = import_module("service")

# Emit a clear deprecation warning when the old package name is used.
# This helps downstream consumers migrate to `service.*` while keeping a
# short compatibility window. We'll remove this shim once callers are
# updated.
warnings.warn(
    "The `zennlogic_ai_service` package name is deprecated; import `service` instead.",
    DeprecationWarning,
    stacklevel=2,
)

# Use the service package's path so submodules are found under this name.
# mypy expects __path__ to be a concrete list[str]; importlib sets it to a
# MutableSequence[str]. Convert to a plain list to satisfy static type
# checkers while preserving runtime behavior.
__path__ = list(_service.__path__)

# Re-export top-level attributes for convenience (not strictly necessary,
# but can help some import styles).
for _name in dir(_service):
    if not _name.startswith("_") and _name not in globals():
        try:
            globals()[_name] = getattr(_service, _name)
        except Exception:
            # Best-effort; ignore failures to avoid import-time crashes
            pass
