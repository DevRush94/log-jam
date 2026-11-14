with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Let's inspect all script code and check every variable initialization
# Are there any ReferenceErrors or TypeError before DOMContentLoaded or inside DOMContentLoaded?
script_start = html.find("<script>") + len("<script>")
script_end = html.find("</script>")
js_code = html[script_start:script_end]

print("Total JS code length:", len(js_code))

