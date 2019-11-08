#!/usr/bin/python
import os
import sys

import django

from tests import DJETTestSuiteRunner

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
    django.setup()
    failures = DJETTestSuiteRunner().run_tests(["tests"])
    sys.exit(bool(failures))
