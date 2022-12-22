"""
Sync addresses with pihole
"""
import sys
from pathlib import Path


from structlog import get_logger


from .models import HostDataModel, YamlHost, YamlMapping
from .file import load_config, load_mapping, write_mapping, write_hosts
from . import network

log = get_logger()


def check_file_data(path: Path, hosts: list[HostDataModel]) -> YamlMapping:
    """
    Check file data
    """
    log.info("Checking if hosts mapping file exists")
    if not path.is_file():
        log.info("Config file not found..Creating new file", path=path)
        make_new_mapping_file(path, hosts)
    stored_data = load_mapping(path)
    new_entries = find_new_entries(stored_data.hosts, hosts)
    return add_new_entries(stored_data, new_entries)


def make_new_mapping_file(path: Path, hosts: list[HostDataModel]):
    """
    Make a new mapping file and quit
    """
    parsed_hosts = []
    for host in hosts:
        parsed_hosts.append(YamlHost(mac=host.mac, ip=host.ip))
    output_data = YamlMapping(hosts=parsed_hosts)
    write_mapping(path, output_data)
    log.info(
        "Host Data file sucessfully created and chmod set to 666, please fill in and then rerun"
    )
    sys.exit()


def find_new_entries(
    stored_hosts: list[YamlHost], scanned_hosts: list[HostDataModel]
) -> list[HostDataModel]:
    """
    Check if there are any new entries and add if so
    """

    def check_exists(item):

        result = next((x for x in stored_hosts if x.ip == item.ip), None)
        if result is None:
            return item
        return None

    data = map(check_exists, scanned_hosts)
    new_hosts = [i for i in data if i is not None]

    log.info("New Hosts Found", count=len(new_hosts))
    return new_hosts


def add_new_entries(stored_data: YamlMapping, new_entries: list[HostDataModel]):
    """
    Add new entries to file
    """
    for entry in new_entries:
        stored_data.hosts.append(YamlHost(mac=entry.mac, ip=entry.ip))
    return stored_data


def generate_hosts_data(data: YamlMapping):
    """
    Generate Hosts File
    """
    output = ""
    for host in data.hosts:
        if host.domain is not None:
            if data.tld is None:
                output += f"{host.ip} {host.domain}\n"
            output += f"{host.ip} {host.domain}.{data.tld}\n"
    log.info(
        "Generated Hosts File",
        host_count=len(data.hosts),
        named_hosts=output.count("\n"),
    )
    return output


def main():
    """
    Application Entrypoint
    """
    log.info("Welcome to Sync App")
    config = load_config()
    address, prefix = network.get_interface_address(config.interface_name)

    host_data = network.scan_arp(address, prefix)

    yaml_data = check_file_data(config.mapping_path, host_data)
    string_data = generate_hosts_data(yaml_data)
    write_hosts(config.hosts_path, string_data)
