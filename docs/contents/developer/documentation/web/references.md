# References

## Internal hyperlinks or references within the same document

### References to sections

No matter the document format, markdown or jupyter notebook, you can create internal hyperlinks to sections within the
same document. This is typically done using anchors or IDs.

The anchor is usually generated from the section title by converting it to lowercase, replacing spaces with hyphens, and
removing special characters. For example, a section titled "My Section" would have an anchor like `#my-section`.

You can create a link to this section using the following markdown syntax:

```markdown
(sec-periodic-boundary-conditions)=
# Periodic Boundary Conditions
```

You can then link to this section from anywhere in the document using:

```markdown
See the section on [Periodic Boundary Conditions](#sec-periodic-boundary-conditions)
```
