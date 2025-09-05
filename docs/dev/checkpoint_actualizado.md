# ✅ Checkpoint de corrección de docstrings (actualizado)

Este documento consolida las convenciones y aprendizajes para corregir y estandarizar docstrings en las funciones y clases de **MolSysMT**, según lo trabajado hasta el momento. Úsalo como referencia inicial en futuras sesiones para asegurar continuidad y coherencia.

---

## 📌 Guía de estilo y convenciones

### ✍️ Formato general

- **Formato**: NumPy + Sphinx/MyST (`Parameters`, `Returns`, `Raises`, `Notes`, `See Also`, `Examples`, `.. versionadded::`)
- **Idioma**: Inglés técnico y directo, siempre en tercera persona
- **Título**: Una sola línea, en **gerundio**, con verbo fuerte: *Retrieving...*, *Setting...*, *Locating...*

### 🧱 Secciones obligatorias

1. **One-line summary**
2. **Extended description** (una o dos frases útiles, sin referencias)
3. **Parameters**
   - No dejar líneas en blanco entre parámetros
   - Tipos en minúscula (`str`, `int`, `bool`, `molecular system`, etc.)
   - Argumentos como `selection`, `structure_indices`, `syntax`, etc. deben tener referencias correctas y explicación completa (ver más abajo)
4. **Returns**
   - Tipo de retorno + descripción clara
   - Si hay múltiples outputs, cada uno en su propia línea
5. **Raises**
   - Incluir siempre si aplica: `NotSupportedFormError`, `ArgumentError`, etc.
6. **Notes**
   - Siempre con guiones `-`
   - Incluir referencias clave (ver más abajo)
7. **See Also**
   - Siempre en infinitivo (`Retrieve`, `Select`, `Remove`, etc.)
   - Descripciones concisas (máximo una línea)
8. **Examples**
   - Usar formato `doctest` (`>>>`)
   - Siempre probados con `pytest --doctest-modules`
   - Usar datos reales o del demo (`alanine dipeptide`, `pentalanine`, `T4 lysozyme`, etc.)
9. **Tutorial (admonition fija)**  
   ```rst
   .. admonition:: Tutorial with more examples

      See the following tutorial for a practical demonstration of how to use this function,
      along with additional examples:
      :ref:`Tutorial_<FunctionName>`
   ```

10. **Version**
   - Siempre: `.. versionadded:: 1.0.0` (u otra versión real)

---

## 📏 Espaciado entre secciones

- Debe haber **una sola línea en blanco** entre secciones (`Parameters`, `Returns`, `Notes`, etc.)
- No se dejan líneas en blanco **dentro** del bloque de parámetros entre cada argumento.

---

## 🧠 Aclaraciones especiales por parámetro

### `molecular_system`
- Siempre incluir:  
  > Molecular system to be analyzed. It can be in any of the :ref:`supported forms <Introduction_Forms>`.

### `selection`
- Puede ser: `str`, `list`, `tuple`, `numpy.ndarray`
- Siempre indicar:
  - Que acepta índices **0-based**
  - Que `'all'` selecciona todos los elementos
  - Incluir referencia: `:ref:`supported selection syntaxes <Introduction_Selection>``

### `structure_indices`
- Igual que `selection`:
  - ÍNDICES **0-based**
  - `'all'` aplica a todas las estructuras
  - Referencia opcional (ya está en Notes)

### `syntax`
- Siempre aclarar que es el selector que se usa para interpretar `selection`
- Incluir:  
  > See :ref:`Introduction_Selection` for details.

### `skip_digestion`
- Texto estándar para todas las funciones:
  ```text
  Whether to skip MolSysMT’s internal argument digestion mechanism.

  MolSysMT includes a built-in digestion system that validates and normalizes
  function arguments. This process checks types, shapes, and values, and automatically
  adjusts them when possible to meet expected formats.

  Setting `skip_digestion=True` disables this process, which may improve performance
  in workflows where inputs are already validated. Use with caution: only set this to
  `True` if you are certain all input arguments are correct and consistent.
  ```

---

## 📚 Notas obligatorias en cada función

Agregar al bloque `Notes`:

- `- Supported molecular-system forms are described in :ref:\`Introduction_Forms\`.`
- `- Selection syntaxes and valid query expressions are described in :ref:\`Introduction_Selection\`.`
- Si aplica:
  - `- If element is not specified, it is inferred from the attribute definition.`
  - `- If the attribute runs over structures, structure_indices must be defined accordingly.`
  - Otras aclaraciones internas como que se devuelve el último ítem coincidente (`where_is_attribute`)

---

## ✅ Funciones revisadas hasta ahora

- `compare`
- `concatenate_structures`
- `contains`
- `convert`
- `copy`
- `extract`
- `get`
- `get_attributes`
- `get_form`
- `get_label`
- `has_attribute`
- `info`
- `is_a_molecular_system`
- `is_composed_of`
- `merge`
- `remove`
- `select` ✅ (completamente revisada y actualizada)
- `set` ✅ (ajustada con todos los detalles y edge cases)
- `view` ✅ (con aclaraciones sobre viewer, selección, etc.)
- `where_is_attribute` ✅ (con revisión exhaustiva y aclaraciones en `Notes`)

**Clase revisada:**
- `Iterator`: (`__init__`, `__iter__`, `__next__`) – ya estandarizada

---

## 🧪 Testing y ejemplos

- Todos los ejemplos deben correr con:
  ```bash
  pytest --doctest-modules
  ```
- Se recomienda usar sistemas del módulo `msm.systems.demo` para no depender de archivos externos

---

## 📘 Referencias clave

- Canonical reference: función `add()` y su tutorial 【`add.md`】
- Guías internas:
  - 【`developer_guide.md`】
  - 【`docstrings.md`】
- Definición del asistente IA y alcance del proyecto: 【`ai_definition_doc.md`】

---

Evita poner palabras en negrita (bold) innecesariamente en los textos descriptivos de los docstrigs.
Especificar en los ejemplos deben ser probados con `pytest --doctest-modules`.
Las opciones '+ELLIPSIS' y 'NORMALIZE_WHITESPACE' fueron incluidas por defecto en el fichero `pytest.ini` (no es necesario repetirlas en el docstring).

Con esto, estamos listos para continuar con los módulos `topology`, `structure`, `attributes`, etc. en futuras sesiones. 🎯

