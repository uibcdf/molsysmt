# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build


.PHONY: help builddir html clean all

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html      to make standalone HTML files"
	@echo "  clean     to clean the directory starting a new compilation from scratch"


builddir:
	mkdir -p $(BUILDDIR)
	@echo "Creating new _build directory"

html: 	builddir
	$(SPHINXBUILD) -b html $(SOURCEDIR) $(SPHINXOPTS) $(BUILDDIR)
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)"

clean:
	rm -rf $(BUILDDIR)
	#rm -rf $(TOOLSPATH)/hash_dict.pickle
	#rm -rf examples/generated/*.rst
	rm -rf api/generated/*.rst




