# Python Makefile

SHELL=/bin/bash
MOD_NAME=m3u_manage
TEST_CMD=nosetests -w $(MOD_NAME) -c etc/tests.cfg --with-coverage --cover-package=$(MOD_NAME)

install:
	python setup.py install

requirements:
	pip install -r requirements.txt

develop:
	pip install -r .requirements-dev.txt

clean:
	rm -rf build dist *.egg-info
	find . -name '*.pyc' -delete
	find . -name __pycache__ -delete

docs:
	rm -rf build/sphinx
	sphinx-build -b html docs build/sphinx

watch:
	watchmedo shell-command -R -p "*.py" -c 'date; $(TEST_CMD); date' .

test:
	$(TEST_CMD)

tox:
	tox

release: clean
	# 1. create API token at https://pypi.org/manage/account/token/
	# 2. create ~/.pypirc with [pypi] / username = __token__ / password = pypi-...
	python setup.py sdist bdist_wheel
	twine upload --config-file ~/.pypirc dist/*

coverage:
	nosetests --with-xcoverage --cover-package=$(MOD_NAME) --cover-tests -c etc/tests.cfg

.PHONY: clean install test watch docs release tox develop homebrew coverage requirements
