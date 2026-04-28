import nbformat
import re
import os

directory = '/home/diego/repos@uibcdf/molsysmt/docs/content/course/00_Common_Core/'
files = sorted([f for f in os.listdir(directory) if f.endswith('.ipynb')])

def replace_residue(text):
    def sub_func(match):
        prefix = match.group(1) or ""
        word = match.group(2)
        if prefix.lower().startswith('amino acid'):
            return prefix + word
        
        # Mapping
        mapping = {
            'residue': 'group',
            'residues': 'groups',
            'Residue': 'Group',
            'Residues': 'Groups',
            'RESIDUE': 'GROUP',
            'RESIDUES': 'GROUPS'
        }
        return prefix + mapping.get(word, word)

    # Match word "residue" or "residues", optionally preceded by "amino acid"
    pattern = re.compile(r'\b((?:amino acid\s+)?)(residues|residue)\b', re.IGNORECASE)
    return pattern.sub(sub_func, text)

def polish_content(text, is_markdown=True):
    # 1. Terminology Standardization
    # Piped/Piped Model
    text = re.sub(r'\bPiped Model\b', 'Composite System', text)
    text = re.sub(r'\bPiped Models\b', 'Composite Systems', text)
    text = re.sub(r'\bpiped model\b', 'composite system', text)
    text = re.sub(r'\bpiped together\b', 'combined', text)
    text = re.sub(r'\bPiped\b', 'Combined Sources', text)
    
    if is_markdown:
        text = replace_residue(text)
    else:
        # In code, only replace if it's in a string or comment?
        # The instruction says "Maintain all code logic".
        # However, MolSysMT uses 'group' as element.
        # Let's be very conservative in code.
        # Only replace in comments.
        lines = text.split('\n')
        new_lines = []
        for line in lines:
            if '#' in line:
                code, comment = line.split('#', 1)
                comment = replace_residue(comment)
                new_lines.append(code + '#' + comment)
            else:
                new_lines.append(line)
        text = '\n'.join(new_lines)

    # 2. Format Modernization
    # mmtf -> bcif.gz
    text = text.replace('mmtf', 'bcif.gz')
    
    # Path systems['T4 lysozyme L99A']['181l.bcif.gz']
    text = re.sub(r"systems\['T4 lysozyme L99A'\]\['181l\.(h5msm|pdb|mmtf)'\]", "systems['T4 lysozyme L99A']['181l.bcif.gz']", text)

    # 3. Visual Standards (Admonitions)
    if is_markdown:
        # Convert > **Note:** Content to ```{note} Content ```
        # Handle multi-line if needed, but start with single line
        text = re.sub(r'> \*\*Note:\*\* (.*)', r'```{note}\n\1\n```', text)
        text = re.sub(r'> \*\*Tip:\*\* (.*)', r'```{tip}\n\1\n```', text)
        text = re.sub(r'> \*\*Warning:\*\* (.*)', r'```{warning}\n\1\n```', text)

    return text

for filename in files:
    path = os.path.join(directory, filename)
    print(f"Polishing {filename}...")
    with open(path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    for cell in nb.cells:
        if cell.cell_type == 'markdown':
            cell.source = polish_content(cell.source, is_markdown=True)
        elif cell.cell_type == 'code':
            cell.source = polish_content(cell.source, is_markdown=False)
            
    with open(path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)

print("Done!")
