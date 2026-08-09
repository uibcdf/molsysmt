---
name: Bug report
about: Something behaves incorrectly, raises where it should not, or contradicts the documentation
title: ""
labels: bug, needs-triage
assignees: ""
---

<!--
Three questions. Answer what you can — a partial report we can reproduce is worth
more than a complete one we cannot. Paste output rather than describing it.
-->

**What** — What goes wrong, in a sentence.


**How** — The shortest snippet that shows it, and the traceback if there is one.

```python
import molsysmt as msm
...
```

```
paste the error here
```

**Why** — Which call or workflow this blocks, and what you did instead.


---

**Environment**

- MolSysMT version: <!-- python -c "import molsysmt; print(molsysmt.__version__)" -->
- Python version:
- Platform:
- Installed with: <!-- conda / pip / from source -->

**Molecular system** — If a file is involved, say which format and roughly how large. A
small file that shows the problem is worth more than a large one that also does.


<!--
What happens next: we reproduce it, then answer here restating the problem as we
verified it, with a link to the working record in devguide/. The analysis lives there;
this issue keeps the state and the resolution.

Please do not report a security problem here. Use GitHub's private security advisories.
-->
