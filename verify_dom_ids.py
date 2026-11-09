# -*- coding: utf-8 -*-
import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Collect all IDs in HTML
html_ids = set(re.findall(r'id=["\']([^"\']+)["\']', content))
print(f"Total HTML IDs defined: {len(html_ids)}")

# Collect all getElementById calls in script
script_content = re.search(r'<script>(.*?)</script>', content, re.DOTALL).group(1)
used_ids = set(re.findall(r'getElementById\(["\']([^"\']+)["\']\)', script_content))
print(f"Total IDs accessed by JS getElementById: {len(used_ids)}")

missing_ids = used_ids - html_ids
if missing_ids:
    print(f"⚠️ WARNING: Missing DOM IDs found: {missing_ids}")
else:
    print("All getElementById references match defined HTML IDs! ✓")

