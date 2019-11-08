#!/usr/bin/python
from django.test.runner import DiscoverRunner


class DJETTestSuiteRunner(DiscoverRunner):
    def setup_test_environment(self, **kwargs):
        super(DJETTestSuiteRunner, self).setup_test_environment(**kwargs)
