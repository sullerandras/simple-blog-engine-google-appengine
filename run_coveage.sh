#!/bin/bash

# run coverage

coverage run --omit=/Applications*,/System*,/Library*,markdown* test_runner.py /usr/local/google_appengine tests

coverage report -m
