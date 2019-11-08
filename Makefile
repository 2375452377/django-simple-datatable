export DJANGO_SETTINGS_MODULE=tests.settings
export PYTHONPATH=.

.PHONY: test

test:
	flake8 easy_datatable --ignore=E501
	coverage run `which django-admin.py` test tests
	coverage report
