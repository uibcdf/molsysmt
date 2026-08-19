# Micro-Governance: simulation_workflow.ipynb

## Purpose
Governance rules, frozen contracts, and testing requirements for `simulation_workflow.ipynb`.

## Inviolable Rules & Contracts
1. **Header Block**: Must begin with anchor `(Cookbook_Simulation_Workflow)=`, title `# Working with OpenMM`, gerund summary, and `:::{versionadded} 1.0.0::: `.
2. **Variable Naming**: The canonical molecular system variable name MUST be `molsys` (or `molsys_A`, `molsys_B` for multi-system contexts).
3. **Execution Safety**: All code cells must execute deterministically without raising errors or requiring long simulation runs.
4. **Closing Block**: Must conclude with a collapsible `:::{seealso}` dropdown referencing related Foundations, Tools, and Showcase units.
