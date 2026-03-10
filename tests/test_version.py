import re

import usas_validator


def test_version() -> None:
    version = usas_validator.__version__
    assert isinstance(version, str)
    assert re.search(r"\d+\.\d+\.\d+$", version) is not None