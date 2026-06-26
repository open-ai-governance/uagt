# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Vinod Dhiman and UAGT contributors
"""Make the scripts/ modules importable from tests."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
