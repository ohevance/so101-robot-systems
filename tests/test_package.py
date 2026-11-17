from importlib.metadata import version

import robot_systems


def test_version_matches_metadata() -> None:
    assert robot_systems.__version__ == version("robot-systems")
