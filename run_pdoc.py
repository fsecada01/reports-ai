import importlib
import os
import pkgutil
from pathlib import Path

import django
import pdoc

os.environ["DJANGO_SETTINGS_MODULE"] = "docs.settings"

django.setup()


def discover_modules(root_pkg: str) -> list[str]:
    mods: list[str] = [root_pkg]
    try:
        pkg = importlib.import_module(root_pkg)
        if hasattr(pkg, "__path__"):
            for m in pkgutil.walk_packages(pkg.__path__, prefix=f"{root_pkg}."):
                mods.append(m.name)
    except Exception as e:  # pragma: no cover
        print(f"WARNING: Failed to walk submodules of {root_pkg}: {e}")
    return mods


out_dir = Path("docs/api")
out_dir.mkdir(parents=True, exist_ok=True)

# Only build Python API here; Markdown pages are handled by docs/make.py
modules = discover_modules("reports_ai")
pdoc.pdoc(*modules, output_directory=out_dir)

# Sanity check: ensure key pages exist to help CI logs
required = [out_dir / "reports_ai.html"]
missing = [str(p) for p in required if not p.exists()]
if missing:
    print("WARNING: Missing generated files:", ", ".join(missing))
