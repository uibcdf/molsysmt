# How to create de original english documentation

A package is needed:
```
pip install sphinx-intl
```

And in the conf.py file three new lines were added:

language = 'en'
locale_dirs =  ['_locale/']
gettext_compact = False

### To translate, two options
https://github.com/SekouD/potranslator
https://www.transifex.com/

### More info on the use of Sphinx-Intl
https://www.youtube.com/watch?v=Nz8zutA55fI    
https://sphinx-intl.readthedocs.io/en/master/index.html    
https://sphinx-intl.readthedocs.io/en/master/index.html
http://www.sphinx-doc.org/en/master/usage/advanced/intl.html



## Building from scratch

make html

## Updating

make html

## Cleaning

make clean

# How to create the translated to spanish documentation

## Building from scratch

make pots
make pots_to_pos
- Translate -
make html_es

## Updating

make pots
make pots_to_pos
- Translate -
make html_es

## Cleaning all
make clean_es



