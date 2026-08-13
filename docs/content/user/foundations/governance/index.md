(user-foundations-06-governance)=
# Governance

Welcome to **Governance**, the foundational module detailing the constitutional rules, physical unit guarantees, argument validation protocols, dependency management architecture, precision standards, and diagnostic monitoring systems of MolSysMT.

Governance establishes the framework's reliability contract: ensuring unit safety across all calculations, enforcing strict public versus private API boundaries, dynamically managing soft third-party dependencies, and monitoring execution health with SMonitor.

---

## **Contents**

- **{doc}`quantities_and_units`**  
  Unit-safety guarantees, canonical internal base units (`nm`, `ps`, `K`, `e`), `pyunitwizard` integration, and fast-track unit bypass.

- **{doc}`argument_digestion`**  
  Centralized argument digestion with `@digest`, input selection interpretation, and the explicit trusted boundary of `skip_digestion=True`.

- **{doc}`public_api_and_lifecycle`**  
  Public versus `_private` module boundaries, `@digest` scope rules, API lifecycle integrity standards, and deprecation policies.

- **{doc}`dependency_management`**  
  Hard versus soft dependencies, central mapping in `molsysmt._depdigest`, lazy loading of third-party libraries, and `@dep_digest` capability enforcement.

- **{doc}`configuration_options`**  
  Global session configuration options via `molsysmt.configure` and contextual environment overrides.

- **{doc}`precision_and_types`**  
  Numeric precision policies (`float32`/`float64`), coordinate array dimension invariants, and string identifier normalization (`*_id` as strings).

- **{doc}`smonitor_and_telemetry`**  
  Real-time diagnostic monitoring, RAM memory pressure warnings (`MemoryPressureWarning`), and execution telemetry managed by SMonitor.

```{eval-rst}
.. toctree::
   :maxdepth: 1
   :hidden:

   Quantities & Units <quantities_and_units.md>
   Argument Digestion <argument_digestion.md>
   Public API & Lifecycle <public_api_and_lifecycle.md>
   Dependency Management <dependency_management.md>
   Configuration Options <configuration_options.md>
   Precision & Data Standards <precision_and_types.md>
   SMonitor & Telemetry <smonitor_and_telemetry.md>
```
