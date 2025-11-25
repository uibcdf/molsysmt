
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional, TextIO, Union
import json
import gzip


CompressionKind = Literal["none", "gzip"]


def _empty_universal_dict() -> Dict[str, Any]:
    """Esquema mínimo de un universal_json.

    Pensado como forma más general y rica que viewer_json, por ejemplo:

    - Metadatos globales (fuentes, referencias, condiciones de simulación).
    - Información topológica extendida.
    - Coordenadas y trayectorias (potencialmente referenciadas o particionadas).
    - Anotaciones, etiquetas, datos de análisis, etc.
    """
    return {
        "version": "0.1",  # versión del esquema universal_json

        # Metadatos globales sobre el sistema
        "metadata": {
            # Ejemplos (a rellenar cuando se defina el estándar):
            # "title": "",
            # "source": "",
            # "authors": [],
            # "references": [],
            # "simulation": {"temperature": ..., "pressure": ..., ...},
        },

        # Descripción de entidades/cadenas/residuos/átomos
        "topology": {
            # Estas estructuras se pueden alinear con la semántica MolSysMT:
            # "entities": [...],
            # "chains": [...],
            # "residues": [...],
            # "atoms": {...}  # similar a viewer_json pero quizá con más campos.
        },

        # Coordenadas y trayectorias (podrían ser una o varias colecciones)
        "coordinates": {
            # Ejemplo:
            # "collections": [
            #   {
            #     "label": "default",
            #     "n_atoms": ...,
            #     "estructures": [...],   # ver cómo se sincroniza con topología
            #   },
            # ]
        },

        # Información de enlaces (podría estar en "topology" o aquí)
        "bonds": {
            # "sets": [
            #   {
            #     "label": "default",
            #     "indexA": [],
            #     "indexB": [],
            #     "order": [],
            #   },
            # ]
        },

        # Anotaciones y datos derivados (opcional)
        "annotations": {
            # "selection_labels": {...},
            # "regions_of_interest": [...],
            # "analysis_results": {...},
        },
    }


@dataclass
class UniversalJSON:
    """Representación JSON-serializable general (universal_json).

    Esta clase define la forma `molsysmt.universal_json`, pensada como una
    descripción más amplia y rica de un sistema molecular y sus datos asociados:

    - Incluye sitio para metadatos, topología, coordenadas, enlaces y anotaciones.
    - No está limitada a un único viewer; busca servir como formato interno
      de intercambio/almacenamiento dentro del ecosistema MolSysMT.
    """

    data: Dict[str, Any] = field(default_factory=_empty_universal_dict)

    # Información de compresión
    compressed: bool = False
    compression: CompressionKind = "none"

    # Descripción esquemática de los campos (para documentación / introspección)
    schema: Dict[str, str] = field(default_factory=lambda: {
        "version": "Versión del esquema universal_json.",
        "metadata": "Metadatos globales del sistema (fuentes, referencias, simulación, etc.).",
        "topology": "Descripción estructural detallada (entidades, cadenas, residuos, átomos).",
        "coordinates": "Colecciones de coordenadas y trayectorias asociadas a la topología.",
        "bonds": "Información sobre enlaces químicos, potencialmente en varios conjuntos.",
        "annotations": "Anotaciones y datos derivados (selecciones, análisis, regiones de interés).",
    })

    def to_dict(self) -> Dict[str, Any]:
        """Devuelve el dict JSON-compatible subyacente."""
        return self.data

    # --- Serialización JSON ---

    def dumps(self, indent: Optional[int] = None) -> str:
        """Devuelve una representación JSON en texto."""
        return json.dumps(self.data, indent=indent)

    def dump(
        self,
        fp: Union[str, TextIO],
        *,
        indent: Optional[int] = None,
        compression: Optional[CompressionKind] = None,
    ) -> None:
        """Vuelca el contenido a un fichero (o ruta) como JSON (opcionalmente comprimido).

        Parámetros
        ----------
        fp : str o archivo de texto
            Ruta al fichero de destino o descriptor de archivo abierto en modo texto.
        indent : int, opcional
            Indentación para el JSON.
        compression : {'none', 'gzip'}, opcional
            Si se indica 'gzip', el contenido se escribe comprimido en gzip.
            Si es None, se usa `self.compression`.
        """
        compression = compression or self.compression

        if isinstance(fp, str):
            if compression == "gzip":
                with gzip.open(fp, "wt", encoding="utf-8") as f:
                    json.dump(self.data, f, indent=indent)
            else:
                with open(fp, "w", encoding="utf-8") as f:
                    json.dump(self.data, f, indent=indent)
        else:
            if compression == "gzip":
                raise ValueError(
                    "Para escritura gzip, pase una ruta (str) o un archivo gzip.bin abierto."
                )
            json.dump(self.data, fp, indent=indent)
