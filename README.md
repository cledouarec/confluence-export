# Confluence exporter

[![Lint](https://github.com/cledouarec/confluence-export/actions/workflows/lint.yml/badge.svg)](https://github.com/cledouarec/jira2confluence-gantt/actions/workflows/lint.yml)
[![Unit tests](https://github.com/cledouarec/confluence-export/actions/workflows/test.yml/badge.svg)](https://github.com/cledouarec/jira2confluence-gantt/actions/workflows/test.yml)

**Table of Contents**
* [Overview](#Overview)
* [Installation](#Installation)
* [Usage](#Usage)
* [Configuration](#Configuration)

## Overview


Confluence exporter is a module and a script used to export pages from
Confluence. All the pages exported are merged in one document.

Currently, only the Pdf exporter is fully functional but it is planned to
support others formats like :
- Word
- Markdown

## Installation

It is recommended to use a virtual environment :
```
python -m venv venv
```
To install the module and the main script, simply do :
```
pip install .
```
For the developers, it is useful to install extra tools like :
* [pre-commit](https://pre-commit.com)
* [pytest](http://docs.pytest.org)

These tools can be installed with the following command :
```
pip install .[dev]
```
The Git hooks can be installed with :
```
pre-commit install
```
The hooks can be run manually at any time :
```
pre-commit run --all-file
```

## Usage

The script with required argument can be started by executing the following
command :
```
./confluence-export my_config.yaml
```

The full list of arguments supported can be displayed with the following
helper :
```
./confluence-export.exe -h
usage: confluence-export [-h] [-v] [--user ATLASSIAN_USER]
                         [--password ATLASSIAN_PASSWORD]
                         [config.yaml]

positional arguments:
  config.yaml           Configuration file

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Verbose mode
  --user ATLASSIAN_USER
                        Define the user to connect to Atlassian server
  --password ATLASSIAN_PASSWORD
                        Define the password to connect to Atlassian server
```

## Configuration

The configuration file support 2 formats :
- [YAML format](https://yaml.org) (Recommended format)
- [JSON format](https://www.json.org)

**_In Yaml :_**
```yaml
Server:
  Confluence: "https://my.confluence.server.com"
Pages to export:
  <Space Key 1>: "Page title 1"
  <Space Key 2>:
    - "Page title 1"
    - "Page title 2"
```
**_In Json :_**
```json
{
  "Server": {
    "Confluence": "https://my.confluence.server.com"
  },
  "Pages to export": {
    "<Space Key 1>": "Page title 1",
    "<Space Key 2>": [
      "Page title 1", 
      "Page title 2"
    ]
  }
}
```

The space key can be found easily in the URL of any page :
```
https://my_confluence_url.com/display/<Space key>/...
```

### Server configuration

The `Server` node will configure the URL of the Confluence server.
For the moment, only the username/password authentication is supported but only
in the command line for security reason.

**_In Yaml :_**
```yaml
Server:
  Confluence: "https://my.confluence.server.com"
```
**_In Json :_**
```json
{
  "Server": {
    "Confluence": "https://my.confluence.server.com"
  }
}
```

#### Server

Main configuration node for server.  
**It is a mandatory field.**

#### Confluence

Define the Confluence server URL to get the pages.  
**It is a mandatory field.**

### Pages to export configuration

The `Pages to export` node will configure the list of pages to export by space.
It could be one page only or a list of pages.

**_In Yaml :_**
```yaml
Pages to export:
  <Space Key 1>: "Page title 1"
  <Space Key 2>:
    - "Page title 2"
    - "Page title 3"
```
**_In Json :_**
```json
{
  "Pages to export": {
    "<Space Key 1>": "Page title 1",
    "<Space Key 2>": [
      "Page title 2",
      "Page title 3"
    ]
  }
}
```

#### Pages to export

Main configuration node for exporter.  
**It is a mandatory field.**

#### \<Space key\>

Define the space key that include the pages to export. The value associated
could be a string or a list of string corresponding to the pages title to
export.  
**It is a mandatory field.**
