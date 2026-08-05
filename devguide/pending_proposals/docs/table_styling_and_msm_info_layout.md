# Styling and Layout Enhancement for `msm.info()` Tables in Web Documentation

**Status:** Approved & Implemented (2026-08-04)  
**Scope:** `docs/_static/custom.css`  
**Related Issue:** Readability and visual elegance of summary tables in compiled web documentation.

---

## 1. Problem Statement

While recent updates to `msm.info()` added `class="dataframe"` (enabling proper light/dark mode adaptation and alternate row shading in PyData Sphinx Theme), two visual issues were identified in compiled documentation:

1. **Unwanted Vertical Gridlines**: PyData Sphinx Theme injected `border-left` and `border-right` styles onto table header and data cells. Vertical gridlines diminished visual elegance compared to clean, horizontal-only divider layouts.
2. **Left-Alignment and Narrow Vertical Padding**: Tables defaulted to left alignment with tight vertical padding (`4px`), lacking the airy, relaxed aesthetic of local Jupyter Notebook rendering.

---

## 2. Design Specifications & Solution

Summary tables produced by `msm.info()` (and general pandas DataFrames rendered in documentation notebooks) meet the following refined design rules:

1. **Centered Container Alignment**: Tables are centered horizontally (`margin-left: auto; margin-right: auto;`) within notebook output cells for visual balance.
2. **Natural Compact Width**: Retains pandas' natural column width (`width: auto`) to avoid stretching sparse tables unnaturally across wide viewports.
3. **Clean Horizontal Divider Aesthetics**: Removes all vertical cell borders (`border-left: none !important; border-right: none !important;`) while preserving top/bottom borders.
4. **Comfortable Cell Padding**: Applies generous padding (`8px 16px`) matching local Jupyter Notebook rendering ("allowing text to breathe").
5. **Theme Adaptability**: Preserves dark/light mode background and alternate row shading via `class="dataframe"`.

---

## 3. Implementation

Applied in [`docs/_static/custom.css`](../../docs/_static/custom.css):

```css
/*********************************************
* Centered DataFrames & Clean Table Layout
*********************************************/
table.dataframe {
  margin-left: auto !important;
  margin-right: auto !important;
  border-collapse: collapse !important;
  margin-top: 1.25rem !important;
  margin-bottom: 1.25rem !important;
}

table.dataframe th,
table.dataframe td {
  border-left: none !important;
  border-right: none !important;
  padding: 8px 16px !important;
}
```
