
#!/bin/bash

# Usa el número de hilos indicado, o toma 1 por defecto
THREADS=${1:-1}
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

find contents/ -name '*.ipynb' | while read -r nb; do
    if [[ ! -f "${nb%.ipynb}.nbconvert.log" || "$nb" -nt "${nb%.ipynb}.nbconvert.log" ]]; then
        echo "$nb"
    fi
done | xargs -I{} -P "$THREADS" bash -c 'run_notebook "$@"' _ {}

echo "Ejecución finalizada. Revisa $LOG_FILE para detalles de errores."
