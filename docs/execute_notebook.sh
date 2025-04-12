#!/bin/bash

export MSM_VIEWS_FROM_HTML_FILES=TRUE

# Función para mostrar el uso del script
usage() {
    echo "Uso: $0 [-f|--force] path/al/notebook.ipynb"
    exit 1
}

# Verificar si se proporcionaron argumentos
if [ $# -lt 1 ] || [ $# -gt 2 ]; then
    usage
fi

# Variables para los argumentos
force=false
nb=""

# Procesar los argumentos
if [ "$1" == "-f" ] || [ "$1" == "--force" ]; then
    force=true
    nb="$2"
else
    nb="$1"
fi

# Verificar que el archivo del notebook exista
if [ -z "$nb" ] || [ ! -f "$nb" ]; then
    echo "Error: el archivo '$nb' no existe."
    exit 1
fi

# Definir el archivo de log asociado al notebook
log_file="${nb%.ipynb}.nbconvert.log"

# Verificar si el notebook debe ejecutarse
if [ "$force" = true ] || [ "$nb" -nt "$log_file" ]; then
    echo "Ejecutando notebook: $nb..."
    jupyter nbconvert --execute --inplace "$nb" && touch "$log_file"
    echo "Ejecución finalizada."
else
    echo "Sin cambios: $nb (use -f para forzar la ejecución)."
fi

