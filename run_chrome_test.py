import subprocess

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
args = [
    chrome_path,
    "--headless=new",
    "--screenshot=C:\\Users\\DELL\\Desktop\\code\\Log-jam\\test_screen.png",
    "--window-size=1280,720",
    "--dump-dom",
    "file:///C:/Users/DELL/Desktop/code/Log-jam/index.html"
]

res = subprocess.run(args, capture_output=True, text=True)
print("Return code:", res.returncode)
print("Stdout length:", len(res.stdout))
print("Stderr:", res.stderr[:500])
with open("dumped_dom.html", "w", encoding="utf-8") as f:
    f.write(res.stdout)
print("Saved dumped_dom.html")
