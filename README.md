# dnssync

The goal of this project is to generate a custom hosts file to be used with a local dns resolver for manually specifying DNS names.

This project uses scapy to send an ARP broadcast packet, and record the results into a yaml file.

The domains which are set in will generate a hosts file when re-run.

This can then be used as a hosts file for pihole's custom DNS file allowing you to register your computer as `my-computer.home` for example.

## Requirements

- scapy requires raw socket acess:
    - root or CAP_NET_RAW given to the application
- poetry to install dependancies

## How to use

1. Clone repo
2. Create virtual env
3. Run `poetry install`
4. Run with `python -m dnssync`


### First Run


On first run it will generate a file with a list of hosts in a file called `hosts.yaml`

```yaml
tld: null
hosts:
  - domain: null
    mac: aa:bb:cc:dd:ee:00
    ip: 192.168.0.2
  - domain: null
    mac: aa:bb:cc:dd:ee:01
    ip: 192.168.0.3
  - domain: null
    mac: aa:bb:cc:dd:ee:02
    ip: 192.168.0.4
```

Edit this file to include the domains that you wish to create rules for:

```yaml
tld: home
hosts:
  - domain: my-computer
    mac: aa:bb:cc:dd:ee:00
    ip: 192.168.0.2
  - domain: null
    mac: aa:bb:cc:dd:ee:01
    ip: 192.168.0.3
  - domain: my-laptop
    mac: aa:bb:cc:dd:ee:02
    ip: 192.168.0.4

```

## Subsequent Runs

It will rescan and add any new found hosts

It will then generate a file called `custom.list` in the hosts file format:

For example:
```
192.168.0.2 my-computer.home
192.168.0.4 my-laptop.home
```

This file can then be copied or symlinked.

pihole uses `/etc/pihole/custom.list` for custom mapping.

I use a docker compose version of pihole and replace that file with a symlink.


## Limitations

Not all hosts may respond to broadcast packets

Ping scan could be a better approach