#!/usr/bin/env bash
set -e
coverage erase
coverage run runtests.py
coverage report -i
