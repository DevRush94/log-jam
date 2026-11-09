with open('build_3d_index.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Scanning for modals & navigation:")
for i, line in enumerate(lines[:1000]):
    if 'id="modal-' in line or 'bottom-nav' in line or 'class="nav-tab' in line:
        print(f"L{i+1}: {line.strip()}")
