# NYU DevOps - Orders
[![Build Status](https://github.com/nyu-devops-order/orders/actions/workflows/tdd-tests.yml/badge.svg)](https://github.com/nyu-devops-order/orders/actions)
[![Build Status](https://github.com/nyu-devops-order/orders/actions/workflows/bdd-tests.yml/badge.svg)](https://github.com/nyu-devops-order/orders/actions)
[![codecov](https://codecov.io/gh/nyu-devops-order/orders/branch/master/graph/badge.svg?token=LRI0KMP6N4)](https://codecov.io/gh/nyu-devops-order/orders)
[![Python](https://img.shields.io/badge/Language-Python-red.svg)](https://python.org/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Open in Remote - Containers](https://img.shields.io/static/v1?label=Remote%20-%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/nyu-devops-order/orders)

### Introduction
This repository maintains the back end for an eCommerce website as a RESTful microservices for the orders resource. An order is a collection of order items where each item represents a product, its quantity, and its price. The microservice supports the complete Create, Read, Update, & Delete (CRUD) lifecycle calls plus List.

## Overview

The `/service` folder contains `models.py` file for the model and a `routes.py` file for the service. The `/tests` folder has test cases for testing the model and the service separately.

## Setup
To bring up the development environment you should clone this repo, change into the repo directory:

```bash
$ git clone https://github.com/nyu-devops/lab-flask-tdd.git
$ cd lab-flask-tdd
```

### Start developing with Visual Studio Code and Docker

Open Visual Studio Code using the `code .` command. VS Code will prompt you to reopen in a container and you should say **yes**. This will take a while as it builds the Docker image and creates a container from it to develop in.

```bash
$ code .
```

## Running the tests
Run the tests using `nosetests`

```shell
$ nosetests
```

Show the line numbers for the code that have not been covered

```shell
$ coverage report -m
```

Manually run `nosetests` with `coverage` (but `setup.cfg` does this already)

```shell
$ nosetests --with-coverage --cover-package=service
```

Check if the Python code follows the PEP8 standard

```shell
$ flake8 --count --max-complexity=10 --statistics service
```

## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
requirements.txt    - list if Python libraries required by your code
config.py           - configuration parameters

service/                   - service python package
├── __init__.py            - package initializer
├── config.py              - global configuration for application
├── models.py              - module with business models
├── routes.py              - module with service routes
└── utils                  - utility package
    ├── cli_commands.py    - explicit command to recreate the tables
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/              - test cases package
├── __init__.py     - package initializer
├── factories.py    - generate fake orders or items with factoryboy
├── test_models.py  - test suite for business models
└── test_routes.py  - test suite for service routes
```

## Information about this repo

These are the RESTful routes for `orders` and `items`
```
Endpoint          Methods  Rule
----------------  -------  -----------------------------------------------------
index             GET      /

list_orders     GET      /orders
create_orders   POST     /orders
get_orders      GET      /orders/<int:order_id>
update_orders   PUT      /orders/<int:order_id>
delete_orders   DELETE   /orders/<int:order_id>

list_items    GET      /orders/<int:order_id>/items
create_items  POST     /orders/<int:order_id>/items
get_items     GET      /orders/<int:order_id>/items/<int:item_id>
update_items  PUT      /orders/<int:order_id>/items/<int:item_id>
delete_items  DELETE   /orders/<int:order_id>/items/<int:item_id>
```

## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
