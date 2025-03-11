#!/bin/bash

echo "Buscando notebooks modificados en contents/..."

# Recorre todos los notebooks en el directorio contents/ y sus subdirectorios
for nb in $(find contents/ -name "*.ipynb"); do
    # Si el notebook ha cambiado después de su última ejecución
    if [[ "$nb" -nt "${nb%.ipynb}.nbconvert.log" ]]; then
        echo "Ejecutando $nb..."
        jupyter nbconvert --execute --inplace "$nb" && touch "${nb%.ipynb}.nbconvert.log"
    else
        echo "Sin cambios: $nb"
    fi
done

echo "Ejecución de notebooks finalizada."

