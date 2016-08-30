.PHONY: clean-pyc test pep8 run dev-run

FLAKE8 := $(shell command -v flake8 2>/dev/null)

all: clean-pyc test dev-run


test:
	pip install -r requirements.txt -q
	python tests.py


pep8:
	$(FLAKE8) --exclude venv --max-line-length=120 .


clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +


run:
	python start_actual.py


dev-run:
	python start_fake.py

