#!/bin/bash

python3.10 -m venv .venv
source .venv/bin/activate
pip install https://github.com/Jackenmen/overleaf-sync/tarball/support_for_versioning
