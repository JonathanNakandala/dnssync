"""
Various Tests
"""
from dnssync import app, models


def test_find_new_entries():
    """
    Test Adding new entires
    """
    stored_hosts = [
        models.YamlHost(ip="192.168.0.1", mac="00:00:00:00:00:00"),
        models.YamlHost(ip="192.168.0.2", mac="00:00:00:00:00:01"),
    ]

    scanned_hosts = [
        models.HostDataModel(ip="192.168.0.1", mac="00:00:00:00:00:01"),
        models.HostDataModel(ip="192.168.0.2", mac="00:00:00:00:00:02"),
        models.HostDataModel(ip="192.168.0.3", mac="00:00:00:00:00:03"),
    ]

    desired_output = [
        models.HostDataModel(ip="192.168.0.3", mac="00:00:00:00:00:03"),
    ]

    output = app.find_new_entries(stored_hosts, scanned_hosts)
    assert output == desired_output

    stored_hosts = [
        models.YamlHost(ip="192.168.0.1", mac="00:00:00:00:00:00"),
        models.YamlHost(ip="192.168.0.2", mac="00:00:00:00:00:01"),
    ]

    scanned_hosts = [
        models.HostDataModel(ip="192.168.0.2", mac="00:00:00:00:00:02"),
        models.HostDataModel(ip="192.168.0.3", mac="00:00:00:00:00:03"),
    ]

    desired_output = [
        models.HostDataModel(ip="192.168.0.3", mac="00:00:00:00:00:03"),
    ]

    output = app.find_new_entries(stored_hosts, scanned_hosts)
    assert output == desired_output
