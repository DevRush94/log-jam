# -*- coding: utf-8 -*-
"""
Assembler for Log Jam: 3D Lumber Empire
Merges CSS, HTML, and modular JS files into a single, production-ready, self-contained index.html
"""

import os
from empire_css import CSS_CONTENT
from empire_html import HTML_MARKUP
from empire_js_data import JS_DATA_AND_AUDIO
from empire_js_three import JS_THREE_ENGINE
from empire_js_logic import JS_GAME_LOGIC
from empire_js_loop import JS_SIMULATION_LOOP

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Log Jam: 3D Lumber Empire</title>
    <!-- Three.js CDN -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
{CSS_CONTENT}
    </style>
</head>
<body>
{HTML_MARKUP}
<script>
{JS_DATA_AND_AUDIO}
{JS_GAME_LOGIC}
{JS_THREE_ENGINE}
{JS_SIMULATION_LOOP}
</script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"Successfully generated index.html ({len(html_template)} bytes)")
