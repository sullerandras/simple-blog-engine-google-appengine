Blog engine for Google App Engine
==

Run end-to-end tests
--

1. install lettuce
2. install selenium driver for python
3. install Firefox
4. run tests with `lettuce` (it will start Firefox)

Run unit tests
--

[Guide](https://developers.google.com/appengine/docs/python/tools/localunittesting)

1. install unittest2:

        pip install unittest2

2. run unit tests:

        python test_runner.py /usr/local/google_appengine tests


Code coverage
--

1. install [coverage](http://pypi.python.org/pypi/coverage):

        pip install coverage

2. run unit tests with coverage:

        coverage run --omit=/Applications*,/System*,/Library*,markdown* test_runner.py /usr/local/google_appengine tests

3. see the coverage report:

        coverage report -m
