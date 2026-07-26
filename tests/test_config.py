from pathlib import Path

from repopulse.config import RepoPulseConfig, load_config, write_default_config


def test_config_defaults_are_reasonable() -> None:
    config = RepoPulseConfig()
    assert config.min_readme_chars == 400
    assert config.fail_under == 70
    assert ".git" in config.ignore


def test_write_and_load_default_config(tmp_path: Path) -> None:
    target = write_default_config(tmp_path)
    assert target.name == ".repopulse.yaml"

    config = load_config(tmp_path)
    assert config.min_readme_chars == 400
    assert config.fail_under == 70
