from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional, TextIO, Union
import json
import gzip

CompressionKind = Literal["none", "gzip"]

def _empty_viewer_dict() -> Dict[str, Any]:
    """Esquema mínimo de un viewer_json.

    Todas las estructuras deben ser JSON-compatibles:
    - dict, list, str, int, float, bool, None.
    """
    return {
        "version": "0.1",  # versión del esquema viewer_json

        # Información por átomo (columnar, longitud = n_atoms)
        "atoms": {
            # IDs internos o externos de átomos
            "atom_id": [],          # List[int] | List[str]
            "atom_name": [],        # List[str]
            "group_ig": [],       # List[int] | List[str]
            "group_name": [],     # List[str]
            "chain_id": [],         # List[str]
            "entity_id": [],        # List[int] | List[str]
            "element_symbol": [],   # List[str] (e.g. "C", "N", "O")
            "formal_charge": [],    # List[int]
        },

        # Información de enlaces (opcional)
        "bonds": {
            # Índices de átomos (0-based) que participan en cada enlace
            "indexA": [],           # List[int]
            "indexB": [],           # List[int]
            # Orden de enlace opcional (1, 2, 3, ...)
            "order": [],            # List[int] (misma longitud que indexA/indexB) o []
        },

        # Lista de frames de coordenadas
        "frames": [
            # Cada frame será un dict con la forma:
            # {
            #     "positions": [[x, y, z], ...],  # List[List[float]], len = n_atoms
            #     "time": 0.0,                    # float o int (opcional)
            #     "cell": {                       # opcional
            #         "a": float,
            #         "b": float,
            #         "c": float,
            #         "alpha": float,
            #         "beta": float,
            #         "gamma": float,
            #     },
            # }
        ],
    }


@dataclass
class ViewerJSON:
    """Representación JSON-serializable mínima para visualización (viewer_json).

    Esta clase define la forma estándar `molsysmt.viewer_json`:

    - `data` almacena la estructura lógica (dict JSON-compatible).
    - El contenido está pensado para herramientas de visualización:
      columnas por átomo, lista de frames con coordenadas y caja opcional.
    - Puede serializarse a texto JSON y opcionalmente comprimirse con gzip.
    """

    data: Dict[str, Any] = field(default_factory=_empty_viewer_dict)

    # Información de compresión
    compressed: bool = False
    compression: CompressionKind = "none"

    # Descripción esquemática de los campos (para documentación / introspección)
    schema: Dict[str, str] = field(default_factory=lambda: {
        "version": "Versión del esquema viewer_json.",
        "atoms": "Dict con campos columnar (por átomo): id, nombre, residuo, cadena, entidad, elemento, carga.",
        "bonds": "Dict opcional con índices de átomos enlazados y orden de enlace.",
        "frames": "Lista de frames con coordenadas, tiempo y caja (cell) opcional.",
    })

    def to_dict(self) -> Dict[str, Any]:
        """Devuelve el dict JSON-compatible subyacente.

        Nota:
        - Todos los valores deben ser tipos JSON (dict, list, str, int, float, bool, None).
        """
        return self.data

    # --- Serialización JSON ---

    def dumps(self, indent: Optional[int] = None) -> str:
        """Devuelve una representación JSON en texto.

        Parámetros
        ----------
        indent : int, opcional
            Indentación para hacer el JSON legible (pretty-print).
        """
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
            # Abrimos nosotros el fichero
            if compression == "gzip":
                with gzip.open(fp, "wt", encoding="utf-8") as f:
                    json.dump(self.data, f, indent=indent)
            else:
                with open(fp, "w", encoding="utf-8") as f:
                    json.dump(self.data, f, indent=indent)
        else:
            # Asumimos que el descriptor ya está gestionado por el usuario
            if compression == "gzip":
                # En este caso delegamos: el usuario debería haber abierto
                # un archivo binario gzip; aquí no forzamos nada.
                raise ValueError(
                    "Para escritura gzip, pase una ruta (str) o un archivo gzip.bin abierto."
                )
            json.dump(self.data, fp, indent=indent)
