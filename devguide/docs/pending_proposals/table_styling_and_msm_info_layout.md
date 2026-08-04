# Styling and Layout Enhancement for `msm.info()` Tables in Web Documentation

**Status:** Proposed / Under Review (2026-08-04)  
**Scope:** `molsysmt/basic/info.py` & `docs/_static/custom.css`  
**Related Issue:** Readability and visual elegance of summary tables in compiled web documentation.

---

## 1. Problem Statement

While recent updates to `msm.info()` added `class="dataframe"` (enabling proper light/dark mode adaptation and alternate row shading in PyData Sphinx Theme), two visual regressions were identified in compiled documentation:

1. **Horizontal Compression**: Tables are rendered with `width: auto`, constraining column widths tightly around short cell contents instead of occupying 100% of the output container width. This leaves text looking squeezed and cluttered.
2. **Vertical Column Gridlines**: The theme injects `border-left` and `border-right` styles onto table header and data cells. Vertical gridlines diminish visual elegance compared to clean, horizontal-only divider layouts.

---

## 2. Proposed Design Specifications

Summary tables produced by `msm.info()` (and general pandas DataFrames rendered in documentation notebooks) should satisfy the following criteria:

1. **Full-Width Container Alignment**: `table.dataframe` must expand to `width: 100%` across the notebook output area.
2. **Clean Horizontal Divider Aesthetics**: Remove all vertical cell borders (`border-left: none`, `border-right: none`) while preserving subtle top/bottom borders.
3. **Comfortable Cell Padding**: Ensure consistent padding (`8px 12px`) for high legibility.
4. **Theme Adaptability**: Maintain existing dark/light mode background and text color CSS variables.

---

## 3. Implementation Plan

### **A. Global Documentation CSS Customization (`docs/_static/custom.css`)**
Inject rules targeting `table.dataframe`:
```css
table.dataframe {
    width: 100% !important;
    border-collapse: collapse;
    margin-top: 1rem;
    margin-bottom: 1rem;
}

table.dataframe th,
table.dataframe td {
    border-left: none !important;
    border-right: none !important;
    padding: 8px 12px !important;
}
```

### **B. `molsysmt/basic/info.py` Styler Defaults**
Update `info()` to embed default table styles so local Jupyter Notebook rendering mirrors the web aesthetic:
```python
return (
    tmp_df.style.hide(axis='index')
    .set_table_attributes('class="dataframe"')
    .set_table_styles([
        {'selector': 'table', 'props': [('width', '100%')]},
        {'selector': 'th, td', 'props': [('border-left', 'none'), ('border-right', 'none'), ('padding', '8px 12px')]}
    ])
)
```
