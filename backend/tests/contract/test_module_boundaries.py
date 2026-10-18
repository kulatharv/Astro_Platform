"""Contract tests enforcing module boundary rules via import-linter."""

import pytest
import subprocess
import sys


def test_import_linter_contracts():
    """Verify import-linter passes all contracts (Vedic library independence & module boundaries)."""
    try:
        import importlinter
    except ImportError:
        pytest.skip("import-linter package not installed in environment")

    result = subprocess.run([sys.executable, "-m", "importlinter", "lint"], capture_output=True, text=True)
    if result.returncode != 0:
        result = subprocess.run(["lint-imports"], capture_output=True, text=True)
    assert result.returncode == 0, f"Import linter contract violation:\n{result.stdout}\n{result.stderr}"

