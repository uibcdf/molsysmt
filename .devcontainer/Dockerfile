# Imagen base oficial de micromamba, muy ligera
FROM mambaorg/micromamba:1.5.8

# Necesario para que VS Code y micromamba trabajen bien juntos
ARG MAMBA_DOCKERFILE_ACTIVATE=1

# Usar bash como shell
SHELL ["/bin/bash", "-lc"]

# Opcional: instala utilidades de sistema mínimas
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    git build-essential ca-certificates curl wget \
 && rm -rf /var/lib/apt/lists/*
USER ${MAMBA_USER}
