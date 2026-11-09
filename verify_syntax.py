# -*- coding: utf-8 -*-
import subprocess
import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Extract JS code
scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
print(f"Found {len(scripts)} inline script blocks.")

for i, code in enumerate(scripts):
    temp_js_path = f"temp_check_{i}.js"
    with open(temp_js_path, "w", encoding="utf-8") as tf:
        tf.write(code)
    
    res = subprocess.run(["node", "--check", temp_js_path], capture_output=True, text=True)
    if res.returncode == 0:
        print(f"Script #{i+1}: Node.js syntax check PASSED! ✓")
    else:
        print(f"Script #{i+1}: Node.js syntax error ✗:")
        print(res.stderr)

print("Verification complete.")
