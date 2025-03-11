#!/bin/bash

export MSM_VIEWS_FROM_HTML_FILES=TRUE

# Función para mostrar el uso del script
usage() {
    echo "Uso: $0 [-f|--force] [NÚMERO_DE_HILOS]"
    echo "  -f, --force   Fuerza la ejecución de todos los notebooks."
    echo "  NÚMERO_DE_HILOS (opcional, por defecto 1) define el número de notebooks ejecutándose en paralelo."
    exit 1
}

# Parsear argumentos
FORCE=false
THREADS=1

while [[ $# -gt 0 ]]; do
    case "$1" in
        -f|--force)
            FORCE=true
            shift
            ;;
        [0-9]*)
            THREADS=$1
            shift
            ;;
        *)
            usage
            ;;
    esac
done

LOG_FILE="notebook_errors.log"

echo "Iniciando ejecución de notebooks con $THREADS hilo(s)..."
echo "Inicio del log de errores: $(date)" > "$LOG_FILE"

run_notebook() {
    nb=$1
    if jupyter nbconvert --execute --inplace "$nb"; then
        touch "${nb%.ipynb}.nbconvert.log"
        echo "Ejecutado correctamente: $nb"
    else
        echo "Error en notebook: $nb" | tee -a "$LOG_FILE"
        echo "----------------------------------------" >> "$LOG_FILE"
    fi
}

export -f run_notebook
export LOG_FILE

# Encuentra notebooks ignorando los que están en .ipynb_checkpoints
if [ "$FORCE" = true ]; then
    # Ejecuta todos los notebooks sin importar .nbconvert.log, ignorando .ipynb_checkpoints
    find contents/ -name '*.ipynb' ! -path "*/.ipynb_checkpoints/*" \
        | xargs -I{} -P "$THREADS" bash -c 'run_notebook "$@"' _ {}
else
    # Ejecuta solo los notebooks que han cambiado desde la última ejecución, ignorando .ipynb_checkpoints
    find contents/ -name '*.ipynb' ! -path "*/.ipynb_checkpoints/*" | while read -r nb; do
        if [[ ! -f "${nb%.ipynb}.nbconvert.log" || "$nb" -nt "${nb%.ipynb}.nbconvert.log" ]]; then
            echo "$nb"
        fi
    done | xargs -I{} -P "$THREADS" bash -c 'run_notebook "$@"' _ {}
fi

echo "Ejecución finalizada. Revisa $LOG_FILE para detalles de errores."


