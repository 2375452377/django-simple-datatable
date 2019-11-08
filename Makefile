export DJANGO_SETTINGS_MODULE=tests.settings
export PYTHONPATH=.

.PHONY: test

test:
	flake8 simple_datatable --ignore=E501
	coverage run `which django-admin.py` test tests
	coverage report

pack: clean
	python setup.py sdist

clean:
	rm -vrf ./build ./dist ./*.egg-info
	find . -name '*.pyc' -delete
	find . -name '*.tgz' -delete
