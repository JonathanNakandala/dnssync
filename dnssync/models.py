"""
Types for Software
"""
import re
from pathlib import Path

from pydantic import BaseModel, validator
from pydantic_yaml import YamlModel


class TomlConfig(BaseModel):
    """
    Config data for Toml
    """

    interface_name: str
    hosts_path: Path
    mapping_path: Path

    @validator("hosts_path", "mapping_path", pre=True)
    @classmethod
    def parse_as_path(cls, value):
        """
        If not a path type, then parse as
        """
        if isinstance(value, Path):
            return value
        return Path(value)


def valid_mac(value: str) -> str:
    """
    Validate if mac is a valid mac address
    """
    if not re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", value.lower()):
        raise ValueError("Invalid Mac Address")
    return value


def mac_validator(field: str) -> classmethod:
    """
    Mac validator helper function
    """
    decorator = validator(field, allow_reuse=True)
    return decorator(valid_mac)


class HostDataModel(BaseModel):
    """
    A host
    """

    mac: str
    ip: str

    _validate_mac = classmethod = mac_validator("mac")


class YamlHost(HostDataModel):
    """
    Hosts
    """

    domain: str | None = None


class YamlMapping(YamlModel):
    """
    Yaml Data
    """

    tld: str | None = None
    hosts: list[YamlHost]
