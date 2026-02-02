# Dependency Management

MolSysMT uses a systematic approach to handle dependencies, ensuring quick startup times and robustness even when optional libraries are missing.

## Core Concepts

- **Hard Dependencies:** Libraries essential for the core functionality (e.g., `numpy`, `pandas`). MolSysMT will not work without them.
- **Soft Dependencies:** Optional libraries that enable specific features (e.g., `openmm`, `mdtraj`). The package loads without them, but specific functions will fail gracefully if invoked.

## Implementation Guide

### 1. Configuration

All dependencies are defined in `molsysmt/config/dependencies.py`. This is the **Single Source of Truth**.

```python
dependencies = {
    'numpy': Dependency('numpy', 'hard', 'numpy', 'numpy'),
    'mdtraj': Dependency('mdtraj', 'soft', 'mdtraj', 'mdtraj'),
}
```

To add a new dependency or change its status (Hard <-> Soft), edit this file.

### 2. The `@requires` Decorator

The preferred way to enforce a soft dependency is using the `@requires` decorator. It serves two purposes:
1.  **Runtime Validation:** Checks if the library is present before execution.
2.  **Metadata:** Tags the function so the system knows what it needs (useful for introspection).

**Standard Usage:**

```python
from molsysmt.dependencies import requires

@requires('mdtraj')
def to_mdtraj_Trajectory(item):
    # Safe lazy import inside the function
    import mdtraj as md
    return md.Trajectory(...)
```

**Conditional Usage (Multi-engine):**

For functions that support multiple backends, use the `when` argument to specify the condition.

```python
@requires('openmm', when={'engine': 'OpenMM'})
@requires('pdbfixer', when={'engine': 'PDBFixer'})
def solvate(item, engine='OpenMM'):
    if engine == 'OpenMM':
        import openmm
        ...
```

### 3. Manual Checks (`check_dependency`)

In rare cases where the decorator is not suitable (e.g., inside a deeply nested block or a class method where decoration is awkward), use `check_dependency`.

```python
from molsysmt.dependencies import check_dependency

def complex_logic():
    # ... code ...
    if condition:
        check_dependency('openmm')
        import openmm
```

### 4. Lazy Imports Rule

**Rule:** Never import a soft dependency at the top level of a module. Always import it inside the function or method that uses it.

*   **Bad:**
    ```python
    import mdtraj  # Crashes if mdtraj is missing!
    def func(): ...
    ```

*   **Good:**
    ```python
    @requires('mdtraj')
    def func():
        import mdtraj
        ...
    ```

### 5. Interaction with `@digest`

When using `@requires` with `@digest`, place `@requires` **below** `@digest` (closer to the function). This ensures `@requires` validates the normalized arguments produced by `@digest`.

```python
@digest()
@requires('openmm', when={'engine': 'OpenMM'})
def my_func(item, engine='openmm'): # User passes 'openmm', digest converts to 'OpenMM'
    ...
```
