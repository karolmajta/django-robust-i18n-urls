.PHONY: docs

all:
	make test
	python setup.py sdist

docs:
	$(MAKE) -C docs html

test:
	python setup.py test
