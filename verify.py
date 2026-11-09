import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

ids_found = set(re.findall(r'id=["\']([a-zA-Z0-9_\-]+)["\']', content))
ids_requested = set(re.findall(r'getElementById\(["\']([a-zA-Z0-9_\-]+)["\']\)', content))

missing = ids_requested - ids_found
print('Requested count:', len(ids_requested))
print('Found count:', len(ids_found))
print('Missing IDs:', missing)
