# Project Voxx CLI

This is a command line interface client for Voxx.

## Installation

```
pip install voxx-cli
```

## Usage

```
voxx-cli --help

usage: voxx-cli [-h] [-addr ADDR] -user USER

Voxx command line interface client

optional arguments:
  -h, --help  show this help message and exit
  -addr ADDR  Voxx server address
  -user USER  Username to register as
```

Currently, there is a Voxx server instance running at `repo.cyr1en.com:8008`.
To connect to this Voxx server, you can run:

```
voxx-cli -addr repo.cyr1en.com:8008 -user <username>
```