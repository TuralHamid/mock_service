#!/bin/bash

PYTHON_VERSION=$(ls /usr/bin | grep -Eo "python3.[0-9]$")
${PYTHON_VERSION} mock_service.py & disown
