"""
File Operations
"""
import os
from pathlib import Path

import tomli
from structlog import get_logger

from .models import YamlMapping, TomlConfig

log = get_logger()


def load_config() -> TomlConfig:
    """
    Load Configuration
    """
    config_path = Path(__file__).parent.resolve() / "config.toml"
    with open(config_path, "rb") as f_handle:
        data = TomlConfig.parse_obj(tomli.load(f_handle))
        log.info("Configuration Sucessfully Loaded", path=config_path)
        return data


def load_mapping(path: Path):
    """
    Load mapping file
    """
    return YamlMapping.parse_file(path)


def write_mapping(path: Path, data: YamlMapping):
    """
    Write Mapping File to path
    """
    with open(path, "w", encoding="utf8") as f_handle:
        f_handle.write(data.yaml())
    os.chmod(path, 0o666)


def write_hosts(path: Path, data: str):
    """
    Write Hosts file to disk
    """
    with open(path, "w", encoding="utf8") as f_handle:
        f_handle.write(data)
    os.chmod(path, 0o666)
