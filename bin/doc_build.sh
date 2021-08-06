#!/usr/bin/env bash
set -x
mkdir -p BUILD/doc/build
sphinx-build -a -b html ./doc BUILD/doc/build/
