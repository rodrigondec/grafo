docs.build:
	sphinx-build docs/source/ docs/

docs.autodoc:
	sphinx-apidoc -f -o docs/source .

