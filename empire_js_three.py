# -*- coding: utf-8 -*-
JS_THREE_ENGINE = r'''
// ==========================================
// 3. THREE.JS 3D ENGINE & SCENE ARCHITECTURE (RECONSTRUCTED)
// ==========================================
let scene, camera, renderer, overlayCanvas, overlayCtx;
let currentLookAt = new THREE.Vector3(1.2, 1.8, 1.0);
let targetLookAt = new THREE.Vector3(1.2, 1.8, 1.0);
let targetCamPos = new THREE.Vector3(13.5, 23.0, 25.5);

let isDragging = false;
let hasDragged = false;
let prevPointerPos = { x: 0, y: 0 };
let currentZone = "overview";

// 3D Objects & Meshes
let sawMeshes = [];
let towerStackMeshes = [];
let worldPadMeshes = [];
let trucks3D = [];
let rollingLogs3D = [];
let cargoShipMesh = null;
let gantryCraneGroup = null;
let lumberjackMesh = null;
let forkliftMesh = null;
let helicopterMesh = null;
let riverMesh = null;
let pointingHandSprite = null;
let forestTrees = [];

// Overlay 2D Particles & Text
class Particle2D {
    constructor(x, y, vx, vy, color, size, life) {
        this.x = x; this.y = y;
        this.vx = vx; this.vy = vy;
        this.color = color;
        this.size = size;
        this.life = life;
        this.maxLife = life;
    }
    update(dt) {
        this.x += this.vx * dt * 60;
        this.y += this.vy * dt * 60;
        this.vy += 0.18; // gravity
        this.life -= dt;
        return this.life > 0;
    }
    draw(ctx) {
        const alpha = Math.max(0, this.life / this.maxLife);
        ctx.fillStyle = this.color;
        ctx.globalAlpha = alpha;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = 1.0;
    }
}

class FloatingText2D {
    constructor(x, y, text, color = "#10b981", size = 18) {
        this.x = x; this.y = y;
        this.text = text;
        this.color = color;
        this.size = size;
        this.life = 1.3;
        this.maxLife = 1.3;
    }
    update(dt) {
        this.y -= 36 * dt;
        this.life -= dt;
        return this.life > 0;
    }
    draw(ctx) {
        const alpha = Math.max(0, this.life / this.maxLife);
        ctx.save();
        ctx.font = `900 ${this.size}px sans-serif`;
        ctx.textAlign = "center";
        ctx.fillStyle = this.color;
        ctx.shadowColor = "rgba(0,0,0,0.85)";
        ctx.shadowBlur = 6;
        ctx.globalAlpha = alpha;
        ctx.fillText(this.text, this.x, this.y);
        ctx.restore();
    }
}

let particles2D = [];
let floatingTexts2D = [];

function init3DScene() {
    const canvas = document.getElementById("webgl-canvas");
    overlayCanvas = document.getElementById("overlay-canvas");
    overlayCtx = overlayCanvas.getContext("2d");

    // Scene & Fog (Soft sky blue atmosphere)
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xdbeafe);
    scene.fog = new THREE.FogExp2(0xdbeafe, 0.008);

    // Camera (Matching exact isometric view from reference)
    camera = new THREE.PerspectiveCamera(36, window.innerWidth / window.innerHeight, 1, 300);
    camera.position.set(13.5, 23.0, 25.5);
    camera.lookAt(1.2, 1.8, 1.0);

    // Renderer
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false, powerPreference: "high-performance" });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    // Lighting (Crisp cartoon daylight with warm directional shadows)
    const ambientLight = new THREE.HemisphereLight(0xffffff, 0x475569, 0.9);
    scene.add(ambientLight);

    const sunLight = new THREE.DirectionalLight(0xfff7ed, 1.35);
    sunLight.position.set(35, 55, 30);
    sunLight.castShadow = true;
    sunLight.shadow.mapSize.width = 2048;
    sunLight.shadow.mapSize.height = 2048;
    sunLight.shadow.camera.near = 10;
    sunLight.shadow.camera.far = 140;
    sunLight.shadow.camera.left = -40;
    sunLight.shadow.camera.right = 40;
    sunLight.shadow.camera.top = 40;
    sunLight.shadow.camera.bottom = -40;
    sunLight.shadow.bias = -0.0005;
    scene.add(sunLight);

    const fillLight = new THREE.DirectionalLight(0xbae6fd, 0.45);
    fillLight.position.set(-30, 25, -25);
    scene.add(fillLight);

    buildWorldEnvironment();
    buildWorldMachinery();
    buildWorldUpgradePads();
    init3DPointingHand();
    setup3DControls(canvas);

    window.addEventListener("resize", onWindowResize);
    onWindowResize();

    if (renderer && scene && camera) {
        renderer.render(scene, camera);
    }
}

function onWindowResize() {
    if (!camera || !renderer) return;
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);

    const dpr = Math.min(window.devicePixelRatio, 2);
    overlayCanvas.width = window.innerWidth * dpr;
    overlayCanvas.height = window.innerHeight * dpr;
    overlayCtx.resetTransform();
    overlayCtx.scale(dpr, dpr);
}

// ------------------------------------------
// ENVIRONMENT BUILDER (Aligned with 5xpM-hsYo3w.jpg)
// ------------------------------------------
function buildWorldEnvironment() {
    // 1. Vibrant Cartoon Lime Grass Base
    const grassGeo = new THREE.BoxGeometry(100, 1, 100);
    const grassMat = new THREE.MeshStandardMaterial({ color: 0x55c544, roughness: 0.8 });
    const grassMesh = new THREE.Mesh(grassGeo, grassMat);
    grassMesh.position.y = -0.5;
    grassMesh.receiveShadow = true;
    scene.add(grassMesh);

    // 2. Central Factory Dirt & Gravel Courtyard
    const yardGeo = new THREE.BoxGeometry(20, 0.06, 18);
    const yardMat = new THREE.MeshStandardMaterial({ color: 0xd97706, roughness: 0.9 });
    const yardMesh = new THREE.Mesh(yardGeo, yardMat);
    yardMesh.position.set(0.5, 0.04, 1.0);
    yardMesh.receiveShadow = true;
    scene.add(yardMesh);

    // 3. Forest Dirt Tract (Zone 1)
    const forestGroundGeo = new THREE.BoxGeometry(32, 0.05, 40);
    const forestGroundMat = new THREE.MeshStandardMaterial({ color: 0x78350f, roughness: 0.95 });
    const forestGround = new THREE.Mesh(forestGroundGeo, forestGroundMat);
    forestGround.position.set(-25, 0.03, -15);
    forestGround.receiveShadow = true;
    scene.add(forestGround);

    // 4. Interstate Asphalt Highway (x = 8.5)
    const highwayGeo = new THREE.BoxGeometry(5.2, 0.08, 65);
    const highwayMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.65 });
    const highwayMesh = new THREE.Mesh(highwayGeo, highwayMat);
    highwayMesh.position.set(8.5, 0.05, 0);
    highwayMesh.receiveShadow = true;
    scene.add(highwayMesh);

    // White Dashed Road Lines
    const dashMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
    for (let z = -28; z <= 28; z += 3.5) {
        const dashGeo = new THREE.BoxGeometry(0.3, 0.09, 1.8);
        const dash = new THREE.Mesh(dashGeo, dashMat);
        dash.position.set(8.5, 0.06, z);
        scene.add(dash);
    }

    // 5. River Bridge across Highway
    const bridgeGeo = new THREE.BoxGeometry(6.2, 0.45, 10);
    const bridgeMat = new THREE.MeshStandardMaterial({ color: 0xb45309, roughness: 0.8 });
    const bridge = new THREE.Mesh(bridgeGeo, bridgeMat);
    bridge.position.set(8.5, 0.35, 14);
    bridge.castShadow = true; bridge.receiveShadow = true;
    scene.add(bridge);

    // Bridge Guard Rails
    const railMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8 });
    const r1 = new THREE.Mesh(new THREE.BoxGeometry(0.25, 0.6, 10), railMat);
    r1.position.set(5.5, 0.7, 14);
    const r2 = new THREE.Mesh(new THREE.BoxGeometry(0.25, 0.6, 10), railMat);
    r2.position.set(11.5, 0.7, 14);
    scene.add(r1); scene.add(r2);

    // 6. Sparkling Blue River Canal
    const riverGeo = new THREE.PlaneGeometry(16, 70);
    const riverMat = new THREE.MeshStandardMaterial({ color: 0x0284c7, roughness: 0.1, metalness: 0.3 });
    riverMesh = new THREE.Mesh(riverGeo, riverMat);
    riverMesh.rotation.x = -Math.PI / 2;
    riverMesh.position.set(16.5, 0.02, 0);
    scene.add(riverMesh);

    // Stone Harbor Pier
    const dockGeo = new THREE.BoxGeometry(4, 0.28, 20);
    const dockMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.7 });
    const dock = new THREE.Mesh(dockGeo, dockMat);
    dock.position.set(13.5, 0.15, 3);
    dock.receiveShadow = true;
    scene.add(dock);

    // 7. Ocean Cargo Container Ship 'S.S. LOG JAM'
    buildCargoFreighter();

    // 8. Forest Conifers & Log Cabin
    buildForestTrees();
    buildLogCabin();

    // 9. Corporate HQ & Helipad
    buildCorporateHQ();
}

function buildCargoFreighter() {
    cargoShipMesh = new THREE.Group();

    // Hull (Red waterline + Navy Upper)
    const hullLowerGeo = new THREE.BoxGeometry(4.2, 0.8, 14);
    const hullLowerMat = new THREE.MeshStandardMaterial({ color: 0xb91c1c, roughness: 0.5 });
    const hullLower = new THREE.Mesh(hullLowerGeo, hullLowerMat);
    hullLower.position.y = 0.4;
    hullLower.castShadow = true;
    cargoShipMesh.add(hullLower);

    const hullUpperGeo = new THREE.BoxGeometry(4.4, 1.0, 14);
    const hullUpperMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.4 });
    const hullUpper = new THREE.Mesh(hullUpperGeo, hullUpperMat);
    hullUpper.position.y = 1.2;
    hullUpper.castShadow = true;
    cargoShipMesh.add(hullUpper);

    // Bridge Deck (White)
    const bridgeGeo = new THREE.BoxGeometry(3.6, 1.8, 3.2);
    const bridgeMat = new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.4 });
    const bridge = new THREE.Mesh(bridgeGeo, bridgeMat);
    bridge.position.set(0, 2.5, -4.5);
    bridge.castShadow = true;
    cargoShipMesh.add(bridge);

    // Funnel
    const funnelGeo = new THREE.CylinderGeometry(0.4, 0.4, 1.4, 8);
    const funnelMat = new THREE.MeshStandardMaterial({ color: 0xf59e0b });
    const funnel = new THREE.Mesh(funnelGeo, funnelMat);
    funnel.position.set(0, 3.8, -4.8);
    cargoShipMesh.add(funnel);

    // Shipping Containers in Cargo Hold
    const containerColors = [0xef4444, 0x3b82f6, 0x10b981, 0xf59e0b];
    for (let c = 0; c < 4; c++) {
        const cGeo = new THREE.BoxGeometry(1.5, 1.2, 2.4);
        const cMat = new THREE.MeshStandardMaterial({ color: containerColors[c], roughness: 0.6 });
        const cMesh = new THREE.Mesh(cGeo, cMat);
        const zOffset = -1.5 + (c % 2) * 3.0;
        const xOffset = c < 2 ? -0.9 : 0.9;
        cMesh.position.set(xOffset, 2.1, zOffset);
        cMesh.castShadow = true;
        cargoShipMesh.add(cMesh);
    }

    cargoShipMesh.position.set(17.5, 0, 3);
    scene.add(cargoShipMesh);
}

function buildForestTrees() {
    forestTrees = [];
    const positions = [
        [-34, -32], [-28, -34], [-22, -32], [-16, -34],
        [-36, -26], [-30, -28], [-24, -25], [-18, -27],
        [-38, -20], [-32, -22], [-26, -19], [-20, -21],
        [-36, -14], [-30, -16], [-24, -13], [-18, -15],
        [-38, -8],  [-32, -10], [-26, -7],  [-20, -9],
        [-36, -2],  [-30, -4],  [-24, -1],  [-18, -3],
        [-38, 4],   [-32, 2],   [-26, 5],   [-20, 3]
    ];

    positions.forEach(([tx, tz], idx) => {
        const isRedwood = idx % 5 === 0;
        const tree = createLowPolyPine(tx, tz, isRedwood ? 1.5 : (0.9 + (idx % 3) * 0.2), isRedwood);
        forestTrees.push(tree);
    });
}

function createLowPolyPine(x, z, scale = 1.0, isRedwood = false) {
    const group = new THREE.Group();

    // Trunk
    const trunkGeo = new THREE.CylinderGeometry(0.28 * scale, 0.42 * scale, 1.8 * scale, 6);
    const trunkColor = isRedwood ? 0x7c2d12 : 0x78350f;
    const trunkMat = new THREE.MeshStandardMaterial({ color: trunkColor, roughness: 0.9, flatShading: true });
    const trunk = new THREE.Mesh(trunkGeo, trunkMat);
    trunk.position.y = 0.9 * scale;
    trunk.castShadow = true;
    group.add(trunk);

    // 3 Foliage Cones
    const foliageColors = isRedwood 
        ? [0x991b1b, 0xb91c1c, 0xd97706] 
        : [0x14532d, 0x166534, 0x15803d];

    foliageColors.forEach((col, idx) => {
        const coneGeo = new THREE.ConeGeometry((2.0 - idx * 0.35) * scale, 1.8 * scale, 6);
        const coneMat = new THREE.MeshStandardMaterial({ color: col, roughness: 0.8, flatShading: true });
        const cone = new THREE.Mesh(coneGeo, coneMat);
        cone.position.y = (2.0 + idx * 1.0) * scale;
        cone.castShadow = true;
        group.add(cone);
    });

    group.position.set(x, 0, z);
    group.userData = { initialY: 0, isChopped: false, chopCount: 0 };
    scene.add(group);
    return group;
}

function buildLogCabin() {
    const cabin = new THREE.Group();
    const wallGeo = new THREE.BoxGeometry(4.2, 2.4, 3.8);
    const wallMat = new THREE.MeshStandardMaterial({ color: 0x92400e, roughness: 0.85 });
    const walls = new THREE.Mesh(wallGeo, wallMat);
    walls.position.y = 1.2;
    walls.castShadow = true;
    cabin.add(walls);

    const roofGeo = new THREE.ConeGeometry(3.6, 1.6, 4);
    const roofMat = new THREE.MeshStandardMaterial({ color: 0x451a03, roughness: 0.8, flatShading: true });
    const roof = new THREE.Mesh(roofGeo, roofMat);
    roof.rotation.y = Math.PI / 4;
    roof.position.y = 3.0;
    roof.castShadow = true;
    cabin.add(roof);

    const chimGeo = new THREE.BoxGeometry(0.6, 1.8, 0.6);
    const chimMat = new THREE.MeshStandardMaterial({ color: 0x475569 });
    const chim = new THREE.Mesh(chimGeo, chimMat);
    chim.position.set(1.2, 3.0, 0.7);
    cabin.add(chim);

    cabin.position.set(-20, 0, -22);
    scene.add(cabin);
}

function buildCorporateHQ() {
    const hqGroup = new THREE.Group();
    const bGeo = new THREE.BoxGeometry(8.0, 5.5, 6.0);
    const bMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.3 });
    const bMesh = new THREE.Mesh(bGeo, bMat);
    bMesh.position.y = 2.75;
    bMesh.castShadow = true;
    hqGroup.add(bMesh);

    const winGeo = new THREE.BoxGeometry(7.4, 1.8, 5.8);
    const winMat = new THREE.MeshStandardMaterial({ color: 0x38bdf8, roughness: 0.1, metalness: 0.4 });
    const win1 = new THREE.Mesh(winGeo, winMat);
    win1.position.y = 1.8;
    const win2 = new THREE.Mesh(winGeo, winMat);
    win2.position.y = 4.0;
    hqGroup.add(win1); hqGroup.add(win2);

    // Helipad
    const heliGeo = new THREE.CylinderGeometry(4.0, 4.0, 0.12, 24);
    const heliMat = new THREE.MeshStandardMaterial({ color: 0x1e293b });
    const helipad = new THREE.Mesh(heliGeo, heliMat);
    helipad.position.set(8.5, 0.08, 0);
    helipad.receiveShadow = true;
    hqGroup.add(helipad);

    // Helicopter
    helicopterMesh = new THREE.Group();
    const bodyGeo = new THREE.BoxGeometry(1.4, 1.1, 2.8);
    const bodyMat = new THREE.MeshStandardMaterial({ color: 0x0284c7, roughness: 0.3 });
    const body = new THREE.Mesh(bodyGeo, bodyMat);
    body.position.y = 0.9;
    body.castShadow = true;
    helicopterMesh.add(body);

    const tailGeo = new THREE.BoxGeometry(0.25, 0.35, 1.8);
    const tail = new THREE.Mesh(tailGeo, bodyMat);
    tail.position.set(0, 1.0, -2.0);
    helicopterMesh.add(tail);

    const rotorGeo = new THREE.BoxGeometry(4.2, 0.05, 0.3);
    const rotorMat = new THREE.MeshStandardMaterial({ color: 0x0f172a });
    const rotor = new THREE.Mesh(rotorGeo, rotorMat);
    rotor.position.set(0, 1.6, 0);
    helicopterMesh.userData = { rotor };
    helicopterMesh.add(rotor);

    helicopterMesh.position.set(8.5, 0.08, 0);
    hqGroup.add(helicopterMesh);

    hqGroup.position.set(-25, 0, 16);
    scene.add(hqGroup);
}

// ------------------------------------------
// MACHINERY & ENTITY BUILDER
// ------------------------------------------
function buildWorldMachinery() {
    // 1. Forest Intake Bunker (Spawner) at z = -4.5
    const bunkerGeo = new THREE.BoxGeometry(2.8, 2.4, 2.8);
    const bunkerMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.6 });
    const bunker = new THREE.Mesh(bunkerGeo, bunkerMat);
    bunker.position.set(-13.5, 1.2, -4.5);
    bunker.castShadow = true;
    scene.add(bunker);

    // 2. Industrial Mill Conveyor Bed along X axis at z = -4.5
    const convGeo = new THREE.BoxGeometry(14, 0.45, 1.8);
    const convMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.5 });
    const conv = new THREE.Mesh(convGeo, convMat);
    conv.position.set(-6.5, 0.9, -4.5);
    conv.castShadow = true; conv.receiveShadow = true;
    scene.add(conv);

    // Hazard Yellow Guard Rails
    const railMat = new THREE.MeshStandardMaterial({ color: 0xf59e0b, roughness: 0.4 });
    const rail1 = new THREE.Mesh(new THREE.BoxGeometry(14, 0.25, 0.12), railMat);
    rail1.position.set(-6.5, 1.25, -5.4);
    const rail2 = new THREE.Mesh(new THREE.BoxGeometry(14, 0.25, 0.12), railMat);
    rail2.position.set(-6.5, 1.25, -3.6);
    scene.add(rail1); scene.add(rail2);

    // Mill Overhead Sign: 'LOG JAM LUMBER CO.'
    buildMillhouseSign();

    // 3. Hydraulic Debarker Station
    buildDebarkerStation();

    // 4. Circular Gantry Saws
    updateSaws3D();

    // 5. Active 3D Animated Lumberjack
    buildAnimatedLumberjack();

    // 6. Yellow Overhead Gantry Crane
    buildGantryCrane();

    // 7. Active 3D Forklift
    buildAnimatedForklift();

    // 8. Skyscraper Lumber Tower (Centerpiece at x = 0.5, z = 0.5)
    updateLumberTowers3D();
}

function buildMillhouseSign() {
    const signGroup = new THREE.Group();
    const frameGeo = new THREE.BoxGeometry(9, 1.1, 0.25);
    const frameMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.5 });
    const frame = new THREE.Mesh(frameGeo, frameMat);
    frame.position.y = 4.0;
    signGroup.add(frame);

    const signCanvas = document.createElement("canvas");
    signCanvas.width = 512; signCanvas.height = 96;
    const sctx = signCanvas.getContext("2d");
    sctx.fillStyle = "#0f172a";
    sctx.fillRect(0, 0, 512, 96);
    sctx.fillStyle = "#38bdf8";
    sctx.font = "900 36px sans-serif";
    sctx.textAlign = "center";
    sctx.fillText("🪵 LOG JAM LUMBER CO.", 256, 60);

    const signTex = new THREE.CanvasTexture(signCanvas);
    const signPlaneMat = new THREE.MeshBasicMaterial({ map: signTex });
    const signPlane = new THREE.Mesh(new THREE.PlaneGeometry(8.6, 0.9), signPlaneMat);
    signPlane.position.set(0, 4.0, 0.15);
    signGroup.add(signPlane);

    const p1 = new THREE.Mesh(new THREE.BoxGeometry(0.3, 4.0, 0.3), frameMat);
    p1.position.set(-4.0, 2.0, 0);
    const p2 = new THREE.Mesh(new THREE.BoxGeometry(0.3, 4.0, 0.3), frameMat);
    p2.position.set(4.0, 2.0, 0);
    signGroup.add(p1); signGroup.add(p2);

    signGroup.position.set(-6.5, 0, -4.5);
    scene.add(signGroup);
}

function buildDebarkerStation() {
    const debarkerGroup = new THREE.Group();
    const hoodGeo = new THREE.BoxGeometry(2.2, 2.0, 2.2);
    const hoodMat = new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.6 });
    const hood = new THREE.Mesh(hoodGeo, hoodMat);
    hood.position.y = 1.2;
    hood.castShadow = true;
    debarkerGroup.add(hood);

    const rollerGeo = new THREE.CylinderGeometry(0.35, 0.35, 1.6, 12);
    const rollerMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.2, metalness: 0.7 });
    const r1 = new THREE.Mesh(rollerGeo, rollerMat);
    r1.rotation.x = Math.PI / 2;
    r1.position.set(-0.35, 1.3, 0);
    const r2 = new THREE.Mesh(rollerGeo, rollerMat);
    r2.rotation.x = Math.PI / 2;
    r2.position.set(0.35, 1.3, 0);
    debarkerGroup.userData = { r1, r2 };
    debarkerGroup.add(r1); debarkerGroup.add(r2);

    debarkerGroup.position.set(-11.0, 0, -4.5);
    scene.add(debarkerGroup);
}

function updateSaws3D() {
    sawMeshes.forEach(s => scene.remove(s));
    sawMeshes = [];

    const numSaws = Math.min(6, Math.max(1, gameState.upgrades.sawCount || 1));
    for (let i = 0; i < numSaws; i++) {
        const sawGroup = new THREE.Group();
        const archGeo = new THREE.BoxGeometry(0.35, 2.5, 2.2);
        const archMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.7 });
        const arch = new THREE.Mesh(archGeo, archMat);
        arch.position.y = 1.25;
        arch.castShadow = true;
        sawGroup.add(arch);

        // Flashing Warning Light
        const lightGeo = new THREE.SphereGeometry(0.18, 8, 8);
        const lightMat = new THREE.MeshBasicMaterial({ color: 0xfacc15 });
        const light = new THREE.Mesh(lightGeo, lightMat);
        light.position.set(0, 2.6, 0);
        sawGroup.add(light);

        // Spinning Stainless Steel Blade
        const bladeGeo = new THREE.CylinderGeometry(0.9, 0.9, 0.06, 16);
        const bladeMat = new THREE.MeshStandardMaterial({ color: 0xf1f5f9, roughness: 0.15, metalness: 0.9 });
        const blade = new THREE.Mesh(bladeGeo, bladeMat);
        blade.rotation.x = Math.PI / 2;
        blade.position.y = 1.05;
        sawGroup.add(blade);

        sawGroup.position.set(-8.0 + (i * 1.5), 0, -4.5);
        sawGroup.userData = { blade, light };
        scene.add(sawGroup);
        sawMeshes.push(sawGroup);
    }
}

function buildAnimatedLumberjack() {
    lumberjackMesh = new THREE.Group();

    const bootGeo = new THREE.BoxGeometry(0.32, 0.32, 0.55);
    const bootMat = new THREE.MeshStandardMaterial({ color: 0x1e293b });
    const b1 = new THREE.Mesh(bootGeo, bootMat); b1.position.set(-0.22, 0.16, 0);
    const b2 = new THREE.Mesh(bootGeo, bootMat); b2.position.set(0.22, 0.16, 0);
    lumberjackMesh.add(b1); lumberjackMesh.add(b2);

    const legGeo = new THREE.BoxGeometry(0.28, 0.8, 0.28);
    const legMat = new THREE.MeshStandardMaterial({ color: 0x1d4ed8 });
    const l1 = new THREE.Mesh(legGeo, legMat); l1.position.set(-0.22, 0.65, 0);
    const l2 = new THREE.Mesh(legGeo, legMat); l2.position.set(0.22, 0.65, 0);
    lumberjackMesh.add(l1); lumberjackMesh.add(l2);

    const torsoGeo = new THREE.BoxGeometry(0.8, 1.0, 0.45);
    const torsoMat = new THREE.MeshStandardMaterial({ color: 0xdc2626 });
    const torso = new THREE.Mesh(torsoGeo, torsoMat);
    torso.position.y = 1.5;
    torso.castShadow = true;
    lumberjackMesh.add(torso);

    const headGeo = new THREE.BoxGeometry(0.42, 0.42, 0.42);
    const headMat = new THREE.MeshStandardMaterial({ color: 0xfbcfe8 });
    const head = new THREE.Mesh(headGeo, headMat);
    head.position.y = 2.15;
    lumberjackMesh.add(head);

    const hatGeo = new THREE.BoxGeometry(0.55, 0.22, 0.55);
    const hatMat = new THREE.MeshStandardMaterial({ color: 0xeab308 });
    const hat = new THREE.Mesh(hatGeo, hatMat);
    hat.position.y = 2.4;
    lumberjackMesh.add(hat);

    // Swinging Axe Arm
    const armGroup = new THREE.Group();
    const handleGeo = new THREE.CylinderGeometry(0.05, 0.05, 1.3, 6);
    const handleMat = new THREE.MeshStandardMaterial({ color: 0x78350f });
    const handle = new THREE.Mesh(handleGeo, handleMat);
    handle.position.y = -0.35;
    armGroup.add(handle);

    const bladeGeo = new THREE.BoxGeometry(0.1, 0.35, 0.45);
    const bladeMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, metalness: 0.85 });
    const blade = new THREE.Mesh(bladeGeo, bladeMat);
    blade.position.set(0, -0.85, 0.18);
    armGroup.add(blade);

    armGroup.position.set(0.45, 1.8, 0);
    lumberjackMesh.userData = { armGroup, swingTimer: 0 };
    lumberjackMesh.add(armGroup);

    lumberjackMesh.position.set(-18, 0, -12);
    scene.add(lumberjackMesh);
}

function buildGantryCrane() {
    gantryCraneGroup = new THREE.Group();

    // 4 Steel Legs spanning across Lumber Tower & Truck Dock
    const legGeo = new THREE.BoxGeometry(0.55, 7.0, 0.55);
    const craneMat = new THREE.MeshStandardMaterial({ color: 0xeab308, roughness: 0.4 });
    [[-4.5, -2.8], [5.5, -2.8], [-4.5, 3.8], [5.5, 3.8]].forEach(([lx, lz]) => {
        const leg = new THREE.Mesh(legGeo, craneMat);
        leg.position.set(lx, 3.5, lz);
        leg.castShadow = true;
        gantryCraneGroup.add(leg);
    });

    // Overhead Bridge Beam
    const beamGeo = new THREE.BoxGeometry(11.0, 0.75, 7.0);
    const beam = new THREE.Mesh(beamGeo, craneMat);
    beam.position.set(0.5, 6.9, 0.5);
    beam.castShadow = true;
    gantryCraneGroup.add(beam);

    // Trolley & Red Spreader Hoist Block
    const trolleyGeo = new THREE.BoxGeometry(1.5, 0.5, 1.5);
    const trolleyMat = new THREE.MeshStandardMaterial({ color: 0x0f172a });
    const trolley = new THREE.Mesh(trolleyGeo, trolleyMat);
    trolley.position.set(0.5, 6.5, 0.5);
    gantryCraneGroup.add(trolley);

    const hoistGeo = new THREE.BoxGeometry(2.2, 0.5, 1.3);
    const hoistMat = new THREE.MeshStandardMaterial({ color: 0xef4444 });
    const hoist = new THREE.Mesh(hoistGeo, hoistMat);
    hoist.position.set(0.5, 4.2, 0.5);
    gantryCraneGroup.userData = { trolley, hoist, timer: 0 };
    gantryCraneGroup.add(hoist);

    gantryCraneGroup.position.set(4.0, 0, 0.5);
    scene.add(gantryCraneGroup);
}

function buildAnimatedForklift() {
    forkliftMesh = new THREE.Group();

    const bodyGeo = new THREE.BoxGeometry(1.6, 1.0, 2.4);
    const bodyMat = new THREE.MeshStandardMaterial({ color: 0xfacc15, roughness: 0.4 });
    const body = new THREE.Mesh(bodyGeo, bodyMat);
    body.position.y = 0.75;
    body.castShadow = true;
    forkliftMesh.add(body);

    const cageGeo = new THREE.BoxGeometry(1.4, 1.3, 1.4);
    const cageMat = new THREE.MeshStandardMaterial({ color: 0x1e293b });
    const cage = new THREE.Mesh(cageGeo, cageMat);
    cage.position.set(0, 1.6, -0.2);
    forkliftMesh.add(cage);

    const mastGeo = new THREE.BoxGeometry(1.1, 2.0, 0.18);
    const mast = new THREE.Mesh(mastGeo, cageMat);
    mast.position.set(0, 1.3, 1.3);
    forkliftMesh.add(mast);

    const forkGeo = new THREE.BoxGeometry(1.3, 0.1, 1.1);
    const forkMat = new THREE.MeshStandardMaterial({ color: 0x475569 });
    const forks = new THREE.Mesh(forkGeo, forkMat);
    forks.position.set(0, 0.35, 1.7);
    forkliftMesh.userData = { forks, patrolProgress: 0 };
    forkliftMesh.add(forks);

    const wheelGeo = new THREE.CylinderGeometry(0.32, 0.32, 0.22, 12);
    const wheelMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.9 });
    [[-0.9, 0.32, 0.75], [0.9, 0.32, 0.75], [-0.9, 0.32, -0.75], [0.9, 0.32, -0.75]].forEach(([wx, wy, wz]) => {
        const wheel = new THREE.Mesh(wheelGeo, wheelMat);
        wheel.rotation.z = Math.PI / 2;
        wheel.position.set(wx, wy, wz);
        forkliftMesh.add(wheel);
    });

    forkliftMesh.position.set(-2.5, 0, 1.5);
    scene.add(forkliftMesh);
}

// ------------------------------------------
// THE SKYSCRAPER LUMBER TOWER (Exact centerpiece matching 5xpM-hsYo3w.jpg)
// ------------------------------------------
function updateLumberTowers3D() {
    towerStackMeshes.forEach(m => scene.remove(m));
    towerStackMeshes = [];

    const tier = WOOD_TIERS[gameState.woodTier];
    const totalProcessed = gameState.stats.logsProcessed || 0;
    // Visibly builds dozens of layers tall
    const layers = Math.min(28, Math.max(3, Math.floor(totalProcessed / 2) + 4));

    for (let l = 0; l < layers; l++) {
        const isOdd = l % 2 === 1;
        // Criss-cross stacked lumber beams
        for (let b = -1; b <= 1; b++) {
            const plankGeo = isOdd 
                ? new THREE.BoxGeometry(3.8, 0.22, 1.0)
                : new THREE.BoxGeometry(1.0, 0.22, 3.8);

            const plankMat = new THREE.MeshStandardMaterial({ 
                color: tier.color, 
                roughness: 0.65,
                metalness: 0.05
            });
            const plank = new THREE.Mesh(plankGeo, plankMat);

            const px = 0.5 + (isOdd ? 0 : b * 1.3);
            const pz = 0.5 + (isOdd ? b * 1.3 : 0);
            plank.position.set(px, 0.12 + l * 0.24, pz);
            plank.castShadow = true;
            plank.receiveShadow = true;
            scene.add(plank);
            towerStackMeshes.push(plank);
        }
    }
}

// ------------------------------------------
// 3D IN-WORLD DIEGETIC UPGRADE PADS (Matching 5xpM-hsYo3w.jpg)
// ------------------------------------------
function buildWorldUpgradePads() {
    worldPadMeshes = [];
    WORLD_UPGRADE_PADS.forEach(pad => {
        const group = new THREE.Group();

        // 3D Beveled Rounded Box
        const padGeo = new THREE.BoxGeometry(3.6, 0.35, 2.5);
        const padMat = new THREE.MeshStandardMaterial({ color: 0x10b981, roughness: 0.4 });
        const padMesh = new THREE.Mesh(padGeo, padMat);
        padMesh.position.y = 0.17;
        padMesh.castShadow = true; padMesh.receiveShadow = true;
        group.add(padMesh);

        // Dynamic Canvas Label Texture
        const canvasTex = createPadTexture(pad);
        const tex = new THREE.CanvasTexture(canvasTex);
        const labelMat = new THREE.MeshBasicMaterial({ map: tex, transparent: true });
        const labelGeo = new THREE.PlaneGeometry(3.4, 2.3);
        const labelMesh = new THREE.Mesh(labelGeo, labelMat);
        labelMesh.rotation.x = -Math.PI / 2;
        labelMesh.position.y = 0.36;
        group.add(labelMesh);

        group.position.set(pad.pos[0], pad.pos[1], pad.pos[2]);
        group.userData = { pad, padMesh, labelMesh, tex, canvasTex, scaleTimer: 0 };
        scene.add(group);
        worldPadMeshes.push(group);
    });
}

function createPadTexture(pad) {
    const canvas = document.createElement("canvas");
    canvas.width = 256; canvas.height = 192;
    const ctx = canvas.getContext("2d");
    renderPadCanvas(ctx, pad);
    return canvas;
}

function renderPadCanvas(ctx, pad) {
    const def = UPGRADE_DEFS.find(u => u.id === pad.defId);
    const curLv = gameState.upgrades[pad.defId] || 0;
    const isMax = curLv >= (def.maxLv || 100);
    const cost = Math.round(def.baseCost * Math.pow(def.costMult, curLv));
    const canAfford = !isMax && gameState.coins >= cost;

    ctx.clearRect(0, 0, 256, 192);

    ctx.fillStyle = canAfford ? "#10b981" : "#1e293b";
    ctx.beginPath();
    ctx.roundRect(8, 8, 240, 176, 22);
    ctx.fill();

    ctx.strokeStyle = canAfford ? "#6ee7b7" : "rgba(255,255,255,0.2)";
    ctx.lineWidth = canAfford ? 8 : 4;
    ctx.stroke();

    ctx.fillStyle = "#ffffff";
    ctx.font = "900 22px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText(`${pad.icon} ${pad.label}`, 128, 62);

    ctx.fillStyle = canAfford ? "#fef08a" : "#94a3b8";
    ctx.font = "900 32px sans-serif";
    ctx.fillText(isMax ? 'MAX' : `💵 ${formatNumber(cost)}`, 128, 128);
}

function updateWorldPadsUI() {
    worldPadMeshes.forEach(group => {
        const { pad, padMesh, tex, canvasTex } = group.userData;
        const ctx = canvasTex.getContext("2d");
        renderPadCanvas(ctx, pad);
        tex.needsUpdate = true;

        const def = UPGRADE_DEFS.find(u => u.id === pad.defId);
        const curLv = gameState.upgrades[pad.defId] || 0;
        const cost = Math.round(def.baseCost * Math.pow(def.costMult, curLv));
        const canAfford = curLv < (def.maxLv || 100) && gameState.coins >= cost;
        padMesh.material.color.setHex(canAfford ? 0x10b981 : 0x1e293b);
    });
}

// ------------------------------------------
// 3D POINTING HAND HELPER (👆)
// ------------------------------------------
function init3DPointingHand() {
    const canvas = document.createElement("canvas");
    canvas.width = 128; canvas.height = 128;
    const ctx = canvas.getContext("2d");
    ctx.font = "84px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText("👆", 64, 96);

    const tex = new THREE.CanvasTexture(canvas);
    const mat = new THREE.SpriteMaterial({ map: tex, transparent: true });
    pointingHandSprite = new THREE.Sprite(mat);
    pointingHandSprite.scale.set(3.2, 3.2, 1);
    pointingHandSprite.position.set(4.2, 3.5, 5.5);
    pointingHandSprite.visible = false;
    scene.add(pointingHandSprite);
}

// ------------------------------------------
// 3D DELIVERY TRUCK FLEET (Orange Semi-Trucks at x = 8.5)
// ------------------------------------------
class Truck3D {
    constructor(id) {
        this.id = id;
        this.state = "driving_in";
        this.cargo = 0;
        this.isJammed = false;
        this.z = -18 - id * 5.5;
        this.group = new THREE.Group();

        // Cab (Safety Orange)
        const cabGeo = new THREE.BoxGeometry(2.0, 1.6, 2.2);
        const cabMat = new THREE.MeshStandardMaterial({ color: 0xea580c, roughness: 0.3 });
        const cab = new THREE.Mesh(cabGeo, cabMat);
        cab.position.set(0, 1.2, 0.9);
        cab.castShadow = true;
        this.group.add(cab);

        // Windshield
        const glassGeo = new THREE.BoxGeometry(1.8, 0.75, 0.2);
        const glassMat = new THREE.MeshStandardMaterial({ color: 0xe0f2fe, roughness: 0.1 });
        const glass = new THREE.Mesh(glassGeo, glassMat);
        glass.position.set(0, 1.4, 2.0);
        this.group.add(glass);

        // Flatbed (Slate Grey)
        const bedGeo = new THREE.BoxGeometry(2.1, 0.4, 3.6);
        const bedMat = new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.6 });
        const bed = new THREE.Mesh(bedGeo, bedMat);
        bed.position.set(0, 0.8, -1.8);
        bed.castShadow = true;
        this.group.add(bed);

        // 4 Wheels
        const wheelGeo = new THREE.CylinderGeometry(0.38, 0.38, 0.28, 12);
        const wheelMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.9 });
        [[-1.1, 0.38, 0.9], [1.1, 0.38, 0.9], [-1.1, 0.38, -2.4], [1.1, 0.38, -2.4]].forEach(([wx, wy, wz]) => {
            const wheel = new THREE.Mesh(wheelGeo, wheelMat);
            wheel.rotation.z = Math.PI / 2;
            wheel.position.set(wx, wy, wz);
            this.group.add(wheel);
        });

        // 3D Emoji Speech Bubble Billboard
        this.emojiCanvas = document.createElement("canvas");
        this.emojiCanvas.width = 128; this.emojiCanvas.height = 128;
        this.emojiCtx = this.emojiCanvas.getContext("2d");
        this.emojiTex = new THREE.CanvasTexture(this.emojiCanvas);
        const emojiMat = new THREE.SpriteMaterial({ map: this.emojiTex, transparent: true });
        this.emojiSprite = new THREE.Sprite(emojiMat);
        this.emojiSprite.scale.set(2.4, 2.4, 1);
        this.emojiSprite.position.set(0, 3.5, 0);
        this.emojiSprite.visible = false;
        this.group.add(this.emojiSprite);

        this.group.position.set(8.5, 0, this.z);
        scene.add(this.group);
    }

    setEmoji(emoji) {
        if (!emoji) {
            this.emojiSprite.visible = false;
            return;
        }
        this.emojiCtx.clearRect(0, 0, 128, 128);
        this.emojiCtx.fillStyle = emoji === "😡" ? "#ef4444" : "#ffffff";
        this.emojiCtx.beginPath();
        this.emojiCtx.arc(64, 54, 48, 0, Math.PI * 2);
        this.emojiCtx.fill();
        this.emojiCtx.font = "52px sans-serif";
        this.emojiCtx.textAlign = "center";
        this.emojiCtx.fillText(emoji, 64, 72);
        this.emojiTex.needsUpdate = true;
        this.emojiSprite.visible = true;
    }
}

// ------------------------------------------
// CAMERA CONTROLS & ZONE SWITCHER
// ------------------------------------------
const ZONE_PRESETS = {
    overview: { cam: [13.5, 23.0, 25.5], look: [1.2, 1.8, 1.0] },
    sawmill:  { cam: [-2.0, 15.0, 5.0], look: [-5.0, 2.0, -4.5] },
    yard:     { cam: [8.0, 16.0, 14.0], look: [0.5, 2.0, 0.5] },
    highway:  { cam: [12.0, 14.0, 10.0], look: [8.5, 1.5, 0.0] },
    harbor:   { cam: [22.0, 16.0, 12.0], look: [16.5, 2.0, 3.0] },
    forest:   { cam: [-18.0, 16.0, -5.0], look: [-22.0, 1.5, -12.0] },
    hq:       { cam: [-18.0, 16.0, 18.0], look: [-22.0, 2.0, 16.0] }
};

function switchZoneCamera(zoneKey) {
    if (!ZONE_PRESETS[zoneKey]) return;
    currentZone = zoneKey;
    const p = ZONE_PRESETS[zoneKey];
    targetCamPos.set(p.cam[0], p.cam[1], p.cam[2]);
    targetLookAt.set(p.look[0], p.look[1], p.look[2]);

    document.querySelectorAll(".zone-pill").forEach(el => {
        el.classList.toggle("active", el.dataset.zone === zoneKey);
    });
}

function setup3DControls(canvas) {
    canvas.addEventListener("pointerdown", (e) => {
        isDragging = true;
        hasDragged = false;
        prevPointerPos = { x: e.clientX, y: e.clientY };
    });

    window.addEventListener("pointermove", (e) => {
        if (!isDragging) return;
        const dx = e.clientX - prevPointerPos.x;
        const dy = e.clientY - prevPointerPos.y;
        prevPointerPos = { x: e.clientX, y: e.clientY };

        if (Math.abs(dx) > 2 || Math.abs(dy) > 2) {
            hasDragged = true;
            targetCamPos.x -= dx * 0.06;
            targetCamPos.z -= dy * 0.06;
            targetLookAt.x -= dx * 0.06;
            targetLookAt.z -= dy * 0.06;
        }
    });

    window.addEventListener("pointerup", () => {
        isDragging = false;
    });

    window.addEventListener("wheel", (e) => {
        targetCamPos.y = Math.max(10, Math.min(50, targetCamPos.y + e.deltaY * 0.03));
        targetCamPos.z = Math.max(12, Math.min(55, targetCamPos.z + e.deltaY * 0.03));
    }, { passive: true });

    canvas.addEventListener("click", onCanvasClickRaycast);
}

function onCanvasClickRaycast(e) {
    if (hasDragged) { hasDragged = false; return; }

    const rect = renderer.domElement.getBoundingClientRect();
    const mouse = new THREE.Vector2(
        ((e.clientX - rect.left) / rect.width) * 2 - 1,
        -((e.clientY - rect.top) / rect.height) * 2 + 1
    );

    const raycaster = new THREE.Raycaster();
    raycaster.setFromCamera(mouse, camera);

    // 1. Check Upgrade Pads (With bouncy squash & stretch)
    for (const group of worldPadMeshes) {
        const hits = raycaster.intersectObjects(group.children, true);
        if (hits.length > 0) {
            group.scale.set(1.15, 0.75, 1.15);
            setTimeout(() => group.scale.set(1, 1, 1), 180);
            buyUpgrade(group.userData.pad.defId);
            return;
        }
    }

    // 2. Check Trucks (Unjam / Boost)
    for (const truck of trucks3D) {
        const hits = raycaster.intersectObjects(truck.group.children, true);
        if (hits.length > 0) {
            if (truck.isJammed) {
                truck.isJammed = false;
                truck.setEmoji("😊");
                gameState.stats.jamsCleared++;
                const bonus = 200 * (gameState.woodTier + 1);
                gameState.coins += bonus;
                gameState.totalEarned += bonus;
                audio.playSfx('honk');
                audio.playSfx('cash');
                const screenP = toScreenXY(truck.group.position);
                floatingTexts2D.push(new FloatingText2D(screenP.x, screenP.y - 20, `+💵 ${bonus} ZOOM!`, "#34d399", 20));
                setTimeout(() => truck.setEmoji(null), 1400);
            }
            return;
        }
    }

    // 3. Screen Tap Bonus
    gameState.coins += 5;
    gameState.totalEarned += 5;
    audio.playSfx('click');
    floatingTexts2D.push(new FloatingText2D(e.clientX, e.clientY - 10, "+💵 5", "#6ee7b7", 14));
}

function toScreenXY(pos) {
    const v = pos.clone().project(camera);
    return {
        x: (v.x * 0.5 + 0.5) * window.innerWidth,
        y: (-(v.y * 0.5) + 0.5) * window.innerHeight
    };
}
'''
