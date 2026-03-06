import json

nb = json.load(open('project.ipynb', 'r', encoding='utf-8'))
print(f'Total cells: {len(nb["cells"])}')
print("\nFirst 30 cell IDs:")
for i, cell in enumerate(nb['cells'][:30]):
    print(f'{i}: {cell.get("id", "no-id")}')
