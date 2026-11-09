with open('build_index_v2.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Bouncing Hand Pointer
old_pad_draw = 'WORLD_UPGRADE_PADS.forEach(pad => drawWorldUpgradePad(mainCtx, pad));'
new_pad_draw = '''WORLD_UPGRADE_PADS.forEach(pad => drawWorldUpgradePad(mainCtx, pad));

    // Bouncing Hand Pointer (👆) pointing at the urgent upgrade pad during Traffic Jam (matching 5xpM-hsYo3w.jpg)
    if (isTrafficJam || gameState.tutorialStep === 1) {
        const urgentPad = WORLD_UPGRADE_PADS.find(p => p.id === "pad_road" || p.id === "pad_fleet") || WORLD_UPGRADE_PADS[0];
        const pp = toIso(urgentPad.x, urgentPad.y, 0.3);
        const handBounce = Math.sin(Date.now() * 0.01) * 8;
        mainCtx.save();
        mainCtx.font = "34px sans-serif";
        mainCtx.textAlign = "center";
        mainCtx.shadowColor = "rgba(0,0,0,0.6)";
        mainCtx.shadowBlur = 6;
        mainCtx.fillText("👆", pp.x, pp.y - 32 + handBounce);
        mainCtx.restore();
    }'''

text = text.replace(old_pad_draw, new_pad_draw)

# 2. Interactive Tutorial Step Progression
old_tutorial_toast = '<div id="tutorial-toast">💡 Tap anywhere on the mill or click the green 3D upgrade pads!</div>'
new_tutorial_toast = '<div id="tutorial-toast">👆 Step 1/3: Tap anywhere on the mill to boost speed!</div>'
text = text.replace(old_tutorial_toast, new_tutorial_toast)

# 3. Tutorial progress functions
old_canvas_click = '''function handleCanvasClick(e) {'''
new_canvas_click = '''function updateTutorial() {
    const tut = document.getElementById("tutorial-toast");
    if (!tut) return;
    if (gameState.tutorialStep === 0) {
        tut.textContent = "👆 Step 1/3: Tap anywhere on the mill to boost speed!";
        tut.style.display = "block";
    } else if (gameState.tutorialStep === 1) {
        tut.textContent = "🟩 Step 2/3: Tap the green 3D upgrade pads on the ground!";
        tut.style.display = "block";
    } else if (gameState.tutorialStep === 2) {
        tut.textContent = "🚛 Step 3/3: Watch trucks deliver lumber—clear traffic jams!";
        tut.style.display = "block";
    } else {
        tut.style.display = "none";
    }
}

function handleCanvasClick(e) {
    if (gameState.tutorialStep === 0) {
        gameState.tutorialStep = 1;
        updateTutorial();
    }'''
text = text.replace(old_canvas_click, new_canvas_click)

old_upgrade_success = '''updateShopUI();
    } else {'''
new_upgrade_success = '''if (gameState.tutorialStep === 1) {
            gameState.tutorialStep = 2;
            updateTutorial();
        }
        updateShopUI();
    } else {'''
text = text.replace(old_upgrade_success, new_upgrade_success)

old_delivery_success = '''gameState.stats.deliveries++;'''
new_delivery_success = '''gameState.stats.deliveries++;
                if (gameState.tutorialStep === 2) {
                    gameState.tutorialStep = 3;
                    showToast("🎉 Tutorial Complete! Build your timber empire!");
                    updateTutorial();
                }'''
text = text.replace(old_delivery_success, new_delivery_success)

with open('build_index_v2.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("build_index_v2.py patched with hand pointer and interactive tutorial!")
