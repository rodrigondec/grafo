docs.build:
	sphinx-build sphinx/source/ docs/

docs.autodoc:
	sphinx-apidoc -f -o sphinx/source .

