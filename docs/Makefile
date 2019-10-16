# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build
BUILDDIR_ES   = _build_es


.PHONY: help builddir html builddir_es pots pots_to_pos html_es clean clean_es

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html      to make standalone HTML files"
	@echo "  clean     to clean the directory starting a new compilation from scratch"

builddir:
	mkdir -p $(BUILDDIR)

builddir_es:
	mkdir -p $(BUILDDIR_ES)

html: builddir
	$(SPHINXBUILD) -b html $(SOURCEDIR) $(BUILDDIR)
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)"

html_es: builddir_es
	$(SPHINXBUILD) -Dlanguage='es' -b html $(SOURCEDIR) $(BUILDDIR_ES) 
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR_ES)"

pots:
	$(SPHINXBUILD) -b gettext $(SOURCEDIR) _gettext

pots_to_pos:
	sphinx-intl update -p _gettext -l es

clean:
	rm -rf $(BUILDDIR)
	rm -rf api/_autosummary/*.rst

clean_es:
	rm -rf $(BUILDDIR_ES)

clean_pots_pos:
	rm -rf _gettext _locale

