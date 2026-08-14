(user-foundations-performance-caching-and-memoization)=
# Caching & Memoization

MolSysMT employs internal caching and memoization layers to eliminate repetitive parsing overhead and accelerate iterative queries across workflows.

---

## Selection Query Caching

Parsing human-readable selection syntaxes (such as `'atom_name == "CA" and group_name == "ALA"'`) into Abstract Syntax Trees (ASTs) involves string tokenization and grammar parsing.

To avoid repeating this parsing overhead in loops:

- **AST Memoization**: Compiled selection syntax trees are cached in memory. Subsequent evaluations of identical selection strings reuse the pre-compiled AST instantly.
- **Index Caching**: Frequently queried atom or group selection indices are cached when topology immutability is guaranteed.

---

## Form Capability and Dynamic Registry Caching

MolSysMT's form digestion system dynamically discovers registered forms, dependency availabilities, and conversion paths in `molsysmt._depdigest`.

- **Registry Caching**: Available conversion paths between forms are memoized upon first lookup.
- **Lazy Module Mapping**: Soft dependencies are imported on demand and cached internally, preventing slow startup times while ensuring fast subsequent calls.
