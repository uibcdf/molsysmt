# Doctests

## Introduction

To ensure that the examples in docstrings remain correct and up to date, we use
`pytest`'s built-in support for **doctest**. Every `Examples` section must be
written in valid Python syntax using the `>>>` prompt, so it can be
automatically tested.


## Testing Examples with `pytest`

### How to run doctests

You can run the doctests across the entire codebase using:

```bash
pytest --doctest-modules
```

This command will:

- Recursively search for Python files.
- Extract any lines starting with `>>>` in docstrings.
- Execute them and compare the output with the expected results.

### Tips

- Make sure your example is minimal but functional.
- Avoid depending on random data or external files unless mock data is provided.
- Use temporary or minimal molecular systems (e.g. from `molsysmt.demo`) when needed.

### Example of a testable docstring

```python
def add(a, b):
    """
    Adding two numbers.

    Parameters
    ----------
    a : int
    b : int

    Returns
    -------
    int

    Examples
    --------
    >>> add(2, 3)
    5
    """
    return a + b
```

Adding well-formed and tested examples helps users understand usage and prevents regressions in the future.
This is how we test this example embeded in the docstring:

```bash
pytest --doctest-modules molsysmt/basic/add.py
```


