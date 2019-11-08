export DJANGO_SETTINGS_MODULE=tests.settings
export PYTHONPATH=.

.PHONY: test

test:
	coverage run --source=easy_datatable `which django-admin.py` test tests
	coverage report
