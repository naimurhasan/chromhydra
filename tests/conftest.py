import json
from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def load():
    return lambda name: json.loads((FIXTURES / f"{name}.json").read_text())
