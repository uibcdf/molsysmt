(developer-index)=
# **Developer Guide**

Welcome to the MolSysMT Developer Guide. This portal provides comprehensive architectural documentation, setup guides, testing standards, and best practices for contributors.

---

## **Sections**

::::{grid} 1 2 3 3
:gutter: 3

:::{grid-item-card} **Getting Started**
:link: getting_started/index
:link-type: doc

Essential setup instructions, Git workflow, devcontainers, environment bootstrap, and issue reporting.
:::

:::{grid-item-card} **Core Architecture**
:link: core_architecture/index
:link-type: doc

Core design principles, lazy loading via DepDigest, boundary ArgDigest, unit safety, and form adapters.
:::

:::{grid-item-card} **Performance and Scalability**
:link: performance_and_scalability/index
:link-type: doc

Out-of-core trajectory streaming, chunked processing, memory efficiency, and benchmarking suites.
:::

:::{grid-item-card} **Diagnostics and Telemetry**
:link: diagnostics_and_telemetry/index
:link-type: doc

Centralized error handling, SMonitor diagnostic integration, warning catalogs, and structured logging.
:::

:::{grid-item-card} **Testing and Quality Assurance**
:link: testing/index
:link-type: doc

Unit testing workflows with Pytest, local and CI coverage measurement, and validation matrices.
:::

:::{grid-item-card} **Documentation Standards**
:link: documentation/index
:link-type: doc

NumPy docstring guidelines, editorial templates, executable doctests, and MyST web cross-linking.
:::

::::

```{eval-rst}
.. toctree::
   :maxdepth: 2
   :hidden:

   getting_started/index
   core_architecture/index
   performance_and_scalability/index
   diagnostics_and_telemetry/index
   testing/index
   documentation/index
```
