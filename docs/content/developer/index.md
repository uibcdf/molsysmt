# Developer Guide

Welcome to the MolSysMT Developer Guide. This hub provides comprehensive architectural documentation, setup guides, testing standards, and best practices for contributors.

The canonical source of truth for internal governance and tracking remains the `devguide/` directory in the repository.

---

## 1. Getting Started

Essential guides for setting up your development workspace and contributing changes:

| Guide | Description |
| :--- | :--- |
| {doc}`intro/Introduction` | Overview of the developer ecosystem and architectural principles |
| {doc}`intro/fork` | Forking, cloning, editable installation, and Git conventions |
| {doc}`start_dev_env_usage` | Automated environment bootstrap script usage |
| {doc}`devcontainer` | Zero-configuration devcontainers and Codespaces |
| {doc}`reporting` | Issue reporting protocol and devguide lifecycle |

---

## 2. Core Architecture

Design principles and internal frameworks powering MolSysMT:

| Guide | Description |
| :--- | :--- |
| {doc}`dependencies` | Lazy loading architecture and dependency management via DepDigest |
| {doc}`argdigest` | Boundary argument validation and digestion via ArgDigest |
| {doc}`pyunitwizard` | Physical units safety, standard units, and Fast-Track bypass |
| {doc}`element_and_native_rebuild` | Topological element hierarchy and native object rebuild rules |
| {doc}`molsys_builder` | Interactive molecular system builder (`MolSysBuilder`) |
| {doc}`declarative_serialization_forms` | Declarative YAML serialization formats |
| {doc}`new_form` | Step-by-step guide to implementing a new form adapter |

---

## 3. Performance and Scalability

High-performance execution, memory efficiency, and benchmarking:

| Guide | Description |
| :--- | :--- |
| {doc}`heavy_trajectories` | Chunked out-of-core trajectory processing and streaming |
| {doc}`benchmarks` | Performance benchmarking suite and regression testing |

---

## 4. Diagnostics and Telemetry

Centralized error handling, warning catalogs, and structured logging:

| Guide | Description |
| :--- | :--- |
| {doc}`smonitor` | Integration with the SMonitor diagnostic framework |
| {doc}`warnings` | Warning catalogs and profile management |
| {doc}`logging` | Structured diagnostic logging |

---

## 5. Testing and Quality Assurance

Testing workflows, coverage measurement, and continuous integration:

| Guide | Description |
| :--- | :--- |
| {doc}`testing/unit_tests` | Running unit tests with Pytest and fixtures |
| {doc}`testing/code_coverage` | Measuring code coverage locally and via Codecov |
| {doc}`testing/ci` | GitHub Actions CI workflows and validation matrix |

---

## 6. Documentation Standards

Guidelines for writing docstrings, doctests, and web documentation:

| Guide | Description |
| :--- | :--- |
| {doc}`documentation/api/docstrings` | NumPy-style docstring standards and editorial guidelines |
| {doc}`documentation/api/doctests` | Interactive doctest examples and verification |
| {doc}`documentation/web/references` | Cross-linking and section anchor conventions |
| {doc}`documentation/web/myst` | MyST Markdown syntax and interactive elements |

```{eval-rst}
.. toctree::
   :caption: Getting Started
   :hidden:

   intro/index
   intro/Introduction
   intro/fork
   start_dev_env_usage
   devcontainer
   reporting

.. toctree::
   :caption: Core Architecture
   :hidden:

   dependencies
   argdigest
   pyunitwizard
   element_and_native_rebuild
   molsys_builder
   declarative_serialization_forms
   new_form

.. toctree::
   :caption: Performance and Scalability
   :hidden:

   heavy_trajectories
   benchmarks

.. toctree::
   :caption: Diagnostics and Telemetry
   :hidden:

   smonitor
   warnings
   logging

.. toctree::
   :caption: Testing and QA
   :hidden:

   testing/index
   testing/unit_tests
   testing/code_coverage
   testing/ci

.. toctree::
   :caption: Documentation Standards
   :hidden:

   documentation/index
   documentation/api/index
   documentation/api/docstrings
   documentation/api/doctests
   documentation/web/index
   documentation/web/references
   documentation/web/myst
```
