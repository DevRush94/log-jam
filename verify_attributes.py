# -*- coding: utf-8 -*-
import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Check data-zone in zone pills
zones = re.findall(r'data-zone=["\']([^"\']+)["\']', content)
print("Zone pills found:", zones)

# Check data-modal in dock tabs
modals = re.findall(r'data-modal=["\']([^"\']+)["\']', content)
print("Dock tab modals found:", modals)

# Check data-close in modal close buttons
closes = re.findall(r'data-close=["\']([^"\']+)["\']', content)
print("Modal close targets found:", closes)

# Check that every modal exists
for m in modals + closes:
    if f'id="{m}"' not in content:
        print(f"⚠️ Modal target {m} NOT found in HTML!")
print("Attribute checks complete! ✓")

