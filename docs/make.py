"""
Build API documentation using pdoc.

This script mirrors the structure used in SQLModel-CRUD-Utilities but delegates to
the repo's run_pdoc.py to ensure Django is correctly configured during import.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

print("Generating documentation via run_pdoc.py ...")

try:
    result = subprocess.run(
        [sys.executable, str(ROOT / "run_pdoc.py")],
        check=True,
        capture_output=True,
        text=True,
    )
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print("pdoc stderr:")
        print(result.stderr)
    print("Documentation generated successfully (see docs/api/).")
except subprocess.CalledProcessError as e:
    print(f"Error running run_pdoc.py: {e}")
    print("stdout:")
    print(e.stdout)
    print("stderr:")
    print(e.stderr)
    sys.exit(1)

