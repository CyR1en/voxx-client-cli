# Project Voxx CLI

This is a command line interface client for Voxx.

## Installation

```
pip install voxx-cli
```

## Usage

```
Usage: voxx-cli [options] <arg>

-h   --help                      show this help message and exit
-a   --address ADDRESS           voxx server address
-u   --user USERNAME             username to register as
-v   --version                   show program's version number and exit

```

Currently, there is a Voxx server instance running at `repo.cyr1en.com:8008`.
To connect to this Voxx server, you can run:

```
voxx-cli -a repo.cyr1en.com:8008 -u <username>
```