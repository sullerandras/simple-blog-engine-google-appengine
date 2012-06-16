#!/bin/bash

# run unit tests.
# may need to adjust the path for locally installed Google App Engine if
# it is not in /usr/local

python test_runner.py /usr/local/google_appengine tests
