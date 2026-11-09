# -*- coding: utf-8 -*-
JS_THREE_ENGINE = r'''
// ==========================================
// 3. THREE.JS 3D ENGINE & SCENE ARCHITECTURE
// ==========================================
let scene, camera, renderer, overlayCanvas, overlayCtx;
let currentLookAt = new THREE.Vector3(0, 0, 0);
let targetLookAt = new THREE.Vector3(0, 0, 0);
let targetCamPos = new THREE.Vector3(0, 48, 48);

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
        this.vy += 0.15; // gravity
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
        this.life = 1.2;
        this.maxLife = 1.2;
    }
    update(dt) {
        this.y -= 38 * dt;
        this.life -= dt;
        return this.life > 0;
    }
    draw(ctx) {
        const alpha = Math.max(0, this.life / this.maxLife);
        ctx.save();
        ctx.font = `900 ${this.size}px sans-serif`;
        ctx.textAlign = "center";
        ctx.fillStyle = this.color;
        ctx.shadowColor = "rgba(0,0,0,0.8)";
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

    // Scene & Fog
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xdbeafe);
    scene.fog = new THREE.FogExp2(0xdbeafe, 0.007);

    // Camera
    camera = new THREE.PerspectiveCamera(42, window.innerWidth / window.innerHeight, 1, 400);
    camera.position.set(0, 48, 48);
    camera.lookAt(0, 0, 0);

    // Renderer
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false, powerPreference: "high-performance" });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    // Lighting
    const ambientLight = new THREE.HemisphereLight(0xffffff, 0x334155, 0.85);
    scene.add(ambientLight);

    const sunLight = new THREE.DirectionalLight(0xfff7ed, 1.25);
    sunLight.position.set(45, 65, 35);
    sunLight.castShadow = true;
    sunLight.shadow.mapSize.width = 2048;
    sunLight.shadow.mapSize.height = 2048;
    sunLight.shadow.camera.near = 10;
    sunLight.shadow.camera.far = 160;
    sunLight.shadow.camera.left = -55;
    sunLight.shadow.camera.right = 55;
    sunLight.shadow.camera.top = 55;
    sunLight.shadow.camera.bottom = -55;
    sunLight.shadow.bias = -0.0005;
    scene.add(sunLight);

    // Secondary soft fill
    const fillLight = new THREE.DirectionalLight(0xbae6fd, 0.4);
    fillLight.position.set(-40, 30, -30);
    scene.add(fillLight);

    buildWorldEnvironment();
    buildWorldMachinery();
    buildWorldUpgradePads();
    setup3DControls(canvas);

    window.addEventListener("resize", onWindowResize);
    onWindowResize();
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
// ENVIRONMENT BUILDER (160x160 Ground & Sectors)
// ------------------------------------------
function buildWorldEnvironment() {
    // 1. Lush Green Grass Base (160x160)
    const grassGeo = new THREE.BoxGeometry(160, 1, 160);
    const grassMat = new THREE.MeshStandardMaterial({ color: 0x4ade80, roughness: 0.85 });
    const grassMesh = new THREE.Mesh(grassGeo, grassMat);
    grassMesh.position.y = -0.5;
    grassMesh.receiveShadow = true;
    scene.add(grassMesh);

    // 2. Forest Dirt Clearing (Zone 1)
    const forestGroundGeo = new THREE.BoxGeometry(50, 0.05, 60);
    const forestGroundMat = new THREE.MeshStandardMaterial({ color: 0x78350f, roughness: 0.95 });
    const forestGround = new THREE.Mesh(forestGroundGeo, forestGroundMat);
    forestGround.position.set(-35, 0.03, -22);
    forestGround.receiveShadow = true;
    scene.add(forestGround);

    // 3. Central Factory Concrete Yard (Zone 2 & 3)
    const yardGeo = new THREE.BoxGeometry(32, 0.06, 42);
    const yardMat = new THREE.MeshStandardMaterial({ color: 0xd97706, roughness: 0.9 });
    const yardMesh = new THREE.Mesh(yardGeo, yardMat);
    yardMesh.position.set(-2, 0.04, 8);
    yardMesh.receiveShadow = true;
    scene.add(yardMesh);

    // 4. Logistics Apron & Loading Bays (Zone 5)
    const logisticsGeo = new THREE.BoxGeometry(18, 0.07, 36);
    const logisticsMat = new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.7 });
    const logisticsMesh = new THREE.Mesh(logisticsGeo, logisticsMat);
    logisticsMesh.position.set(12, 0.04, 6);
    logisticsMesh.receiveShadow = true;
    scene.add(logisticsMesh);

    // 5. Interstate Asphalt Highway
    const highwayGeo = new THREE.BoxGeometry(6.5, 0.08, 120);
    const highwayMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.6 });
    const highwayMesh = new THREE.Mesh(highwayGeo, highwayMat);
    highwayMesh.position.set(18, 0.05, 0);
    highwayMesh.receiveShadow = true;
    scene.add(highwayMesh);

    // Painted White Dashed Lines
    const dashMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
    for (let z = -50; z <= 50; z += 4) {
        const dashGeo = new THREE.BoxGeometry(0.35, 0.09, 2.0);
        const dash = new THREE.Mesh(dashGeo, dashMat);
        dash.position.set(18, 0.06, z);
        scene.add(dash);
    }

    // 6. Wooden / Concrete Highway River Bridge
    const bridgeGeo = new THREE.BoxGeometry(7.5, 0.45, 16);
    const bridgeMat = new THREE.MeshStandardMaterial({ color: 0xb45309, roughness: 0.8 });
    const bridge = new THREE.Mesh(bridgeGeo, bridgeMat);
    bridge.position.set(18, 0.35, 20);
    bridge.castShadow = true; bridge.receiveShadow = true;
    scene.add(bridge);

    // Bridge Guard Rails
    const railMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.4 });
    const r1 = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.6, 16), railMat);
    r1.position.set(14.5, 0.7, 20);
    const r2 = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.6, 16), railMat);
    r2.position.set(21.5, 0.7, 20);
    scene.add(r1); scene.add(r2);

    // 7. Sparkling River Canal (Zone 4)
    const riverGeo = new THREE.PlaneGeometry(24, 160);
    const riverMat = new THREE.MeshStandardMaterial({ color: 0x0284c7, roughness: 0.1, metalness: 0.25 });
    riverMesh = new THREE.Mesh(riverGeo, riverMat);
    riverMesh.rotation.x = -Math.PI / 2;
    riverMesh.position.set(34, 0.02, 0);
    scene.add(riverMesh);

    // Stone Harbor Pier
    const dockGeo = new THREE.BoxGeometry(5, 0.3, 26);
    const dockMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.7 });
    const dock = new THREE.Mesh(dockGeo, dockMat);
    dock.position.set(24, 0.15, 6);
    dock.receiveShadow = true;
    scene.add(dock);

    // Pier Mooring Bollards
    for (let bz = -4; bz <= 16; bz += 5) {
        const bollardGeo = new THREE.CylinderGeometry(0.2, 0.25, 0.5, 8);
        const bollardMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.5 });
        const bollard = new THREE.Mesh(bollardGeo, bollardMat);
        bollard.position.set(26.2, 0.4, bz);
        scene.add(bollard);
    }

    // 8. Cargo Container Freight Ship 'S.S. LOG JAM'
    buildCargoFreighter();

    // 9. Zone 1: Forest Trees & Log Cabin
    buildForestTrees();
    buildLogCabin();

    // 10. Zone 6: Corporate HQ & Helipad
    buildCorporateHQ();
}

function buildCargoFreighter() {
    cargoShipMesh = new THREE.Group();

    // Hull (Navy with Red Waterline)
    const hullLowerGeo = new THREE.BoxGeometry(4.8, 0.8, 16);
    const hullLowerMat = new THREE.MeshStandardMaterial({ color: 0xb91c1c, roughness: 0.5 });
    const hullLower = new THREE.Mesh(hullLowerGeo, hullLowerMat);
    hullLower.position.y = 0.4;
    hullLower.castShadow = true;
    cargoShipMesh.add(hullLower);

    const hullUpperGeo = new THREE.BoxGeometry(5.0, 1.2, 16);
    const hullUpperMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.4 });
    const hullUpper = new THREE.Mesh(hullUpperGeo, hullUpperMat);
    hullUpper.position.y = 1.3;
    hullUpper.castShadow = true;
    cargoShipMesh.add(hullUpper);

    // Bridge Deck (White)
    const bridgeGeo = new THREE.BoxGeometry(4.2, 2.0, 3.8);
    const bridgeMat = new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.4 });
    const bridge = new THREE.Mesh(bridgeGeo, bridgeMat);
    bridge.position.set(0, 2.8, -5.2);
    bridge.castShadow = true;
    cargoShipMesh.add(bridge);

    // Exhaust Funnel (Yellow with black stripe)
    const funnelGeo = new THREE.CylinderGeometry(0.5, 0.5, 1.6, 8);
    const funnelMat = new THREE.MeshStandardMaterial({ color: 0xf59e0b, roughness: 0.4 });
    const funnel = new THREE.Mesh(funnelGeo, funnelMat);
    funnel.position.set(0, 4.3, -5.5);
    cargoShipMesh.add(funnel);

    // Shipping Containers in Cargo Hold
    const containerColors = [0xef4444, 0x3b82f6, 0x10b981, 0xf59e0b];
    for (let c = 0; c < 4; c++) {
        const cGeo = new THREE.BoxGeometry(1.8, 1.4, 2.8);
        const cMat = new THREE.MeshStandardMaterial({ color: containerColors[c], roughness: 0.6 });
        const cMesh = new THREE.Mesh(cGeo, cMat);
        const zOffset = -1.5 + (c % 2) * 3.4;
        const xOffset = c < 2 ? -1.1 : 1.1;
        cMesh.position.set(xOffset, 2.4, zOffset);
        cMesh.castShadow = true;
        cargoShipMesh.add(cMesh);
    }

    cargoShipMesh.position.set(31, 0, 6);
    scene.add(cargoShipMesh);
}

function buildForestTrees() {
    // Generate 45+ lush low-poly pine & redwood trees in Zone 1
    forestTrees = [];
    const positions = [
        [-46, -42], [-40, -44], [-34, -45], [-28, -42], [-22, -44],
        [-48, -35], [-42, -37], [-35, -34], [-29, -36], [-23, -33],
        [-50, -28], [-44, -29], [-38, -27], [-32, -30], [-26, -26],
        [-48, -20], [-42, -22], [-36, -18], [-30, -21], [-24, -18],
        [-50, -12], [-44, -14], [-38, -10], [-32, -12], [-26, -10],
        [-48, -4],  [-42, -5],  [-36, -2],  [-30, -4],  [-24, -3],
        [-52, 4],   [-45, 2],   [-38, 6],   [-31, 3],   [-25, 5]
    ];

    positions.forEach(([tx, tz], idx) => {
        const isRedwood = idx % 5 === 0;
        const tree = createLowPolyPine(tx, tz, isRedwood ? 1.6 : (0.9 + Math.random() * 0.4), isRedwood);
        forestTrees.push(tree);
    });
}

function createLowPolyPine(x, z, scale = 1.0, isRedwood = false) {
    const group = new THREE.Group();

    // Trunk
    const trunkGeo = new THREE.CylinderGeometry(0.3 * scale, 0.45 * scale, 2.0 * scale, 6);
    const trunkColor = isRedwood ? 0x7c2d12 : 0x78350f;
    const trunkMat = new THREE.MeshStandardMaterial({ color: trunkColor, roughness: 0.9, flatShading: true });
    const trunk = new THREE.Mesh(trunkGeo, trunkMat);
    trunk.position.y = 1.0 * scale;
    trunk.castShadow = true;
    group.add(trunk);

    // 3 Foliage Cones
    const foliageColors = isRedwood 
        ? [0x991b1b, 0xb91c1c, 0xd97706] 
        : [0x14532d, 0x166534, 0x15803d];

    foliageColors.forEach((col, idx) => {
        const coneGeo = new THREE.ConeGeometry((2.2 - idx * 0.4) * scale, 2.0 * scale, 6);
        const coneMat = new THREE.MeshStandardMaterial({ color: col, roughness: 0.8, flatShading: true });
        const cone = new THREE.Mesh(coneGeo, coneMat);
        cone.position.y = (2.2 + idx * 1.1) * scale;
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

    // Base Walls
    const wallGeo = new THREE.BoxGeometry(4.5, 2.6, 4.0);
    const wallMat = new THREE.MeshStandardMaterial({ color: 0x92400e, roughness: 0.85 });
    const walls = new THREE.Mesh(wallGeo, wallMat);
    walls.position.y = 1.3;
    walls.castShadow = true;
    cabin.add(walls);

    // Pitched Roof
    const roofGeo = new THREE.ConeGeometry(3.8, 1.8, 4);
    const roofMat = new THREE.MeshStandardMaterial({ color: 0x451a03, roughness: 0.8, flatShading: true });
    const roof = new THREE.Mesh(roofGeo, roofMat);
    roof.rotation.y = Math.PI / 4;
    roof.position.y = 3.3;
    roof.castShadow = true;
    cabin.add(roof);

    // Chimney with Smoke
    const chimGeo = new THREE.BoxGeometry(0.7, 2.0, 0.7);
    const chimMat = new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.9 });
    const chim = new THREE.Mesh(chimGeo, chimMat);
    chim.position.set(1.4, 3.2, 0.8);
    chim.castShadow = true;
    cabin.add(chim);

    cabin.position.set(-25, 0, -32);
    scene.add(cabin);
}

function buildCorporateHQ() {
    const hqGroup = new THREE.Group();

    // 2-Story Glass Building
    const buildingGeo = new THREE.BoxGeometry(9.0, 6.0, 7.0);
    const buildingMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.3 });
    const bMesh = new THREE.Mesh(buildingGeo, buildingMat);
    bMesh.position.y = 3.0;
    bMesh.castShadow = true;
    hqGroup.add(bMesh);

    // Glass Windows
    const winGeo = new THREE.BoxGeometry(8.2, 2.0, 6.8);
    const winMat = new THREE.MeshStandardMaterial({ color: 0x38bdf8, roughness: 0.1, metalness: 0.4 });
    const win1 = new THREE.Mesh(winGeo, winMat);
    win1.position.y = 2.0;
    const win2 = new THREE.Mesh(winGeo, winMat);
    win2.position.y = 4.4;
    hqGroup.add(win1); hqGroup.add(win2);

    // Helipad Pad
    const heliGeo = new THREE.CylinderGeometry(4.5, 4.5, 0.15, 24);
    const heliMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.7 });
    const helipad = new THREE.Mesh(heliGeo, heliMat);
    helipad.position.set(10.0, 0.08, 0);
    helipad.receiveShadow = true;
    hqGroup.add(helipad);

    // Helipad Yellow Ring
    const ringGeo = new THREE.RingGeometry(3.6, 4.0, 24);
    const ringMat = new THREE.MeshBasicMaterial({ color: 0xf59e0b, side: THREE.DoubleSide });
    const ring = new THREE.Mesh(ringGeo, ringMat);
    ring.rotation.x = -Math.PI / 2;
    ring.position.set(10.0, 0.18, 0);
    hqGroup.add(ring);

    // Executive VIP Helicopter
    helicopterMesh = new THREE.Group();
    const bodyGeo = new THREE.BoxGeometry(1.6, 1.2, 3.2);
    const bodyMat = new THREE.MeshStandardMaterial({ color: 0x0284c7, roughness: 0.3 });
    const body = new THREE.Mesh(bodyGeo, bodyMat);
    body.position.y = 1.0;
    body.castShadow = true;
    helicopterMesh.add(body);

    const tailGeo = new THREE.BoxGeometry(0.3, 0.4, 2.2);
    const tail = new THREE.Mesh(tailGeo, bodyMat);
    tail.position.set(0, 1.2, -2.4);
    helicopterMesh.add(tail);

    // Rotor Blade
    const rotorGeo = new THREE.BoxGeometry(4.8, 0.05, 0.35);
    const rotorMat = new THREE.MeshStandardMaterial({ color: 0x0f172a });
    const rotor = new THREE.Mesh(rotorGeo, rotorMat);
    rotor.position.set(0, 1.8, 0);
    helicopterMesh.userData = { rotor };
    helicopterMesh.add(rotor);

    helicopterMesh.position.set(10.0, 0.08, 0);
    hqGroup.add(helicopterMesh);

    hqGroup.position.set(-36, 0, 22);
    scene.add(hqGroup);
}

// ------------------------------------------
// MACHINERY & ENTITY BUILDER
// ------------------------------------------
function buildWorldMachinery() {
    // 1. Forest Intake Bunker (Spawner)
    const bunkerGeo = new THREE.BoxGeometry(3.2, 2.6, 3.2);
    const bunkerMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.6 });
    const bunker = new THREE.Mesh(bunkerGeo, bunkerMat);
    bunker.position.set(-14, 1.3, -12);
    bunker.castShadow = true;
    scene.add(bunker);

    // 2. Industrial Mill Conveyor Bed
    const convGeo = new THREE.BoxGeometry(16, 0.45, 1.8);
    const convMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.5 });
    const conv = new THREE.Mesh(convGeo, convMat);
    conv.position.set(-6, 0.9, -12);
    conv.castShadow = true; conv.receiveShadow = true;
    scene.add(conv);

    // Hazard Yellow Guard Rails
    const railMat = new THREE.MeshStandardMaterial({ color: 0xf59e0b, roughness: 0.4 });
    const rail1 = new THREE.Mesh(new THREE.BoxGeometry(16, 0.25, 0.12), railMat);
    rail1.position.set(-6, 1.25, -12.9);
    const rail2 = new THREE.Mesh(new THREE.BoxGeometry(16, 0.25, 0.12), railMat);
    rail2.position.set(-6, 1.25, -11.1);
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

    // 8. Skyscraper Lumber Stacks
    updateLumberTowers3D();
}

function buildMillhouseSign() {
    const signGroup = new THREE.Group();
    const frameGeo = new THREE.BoxGeometry(10, 1.2, 0.3);
    const frameMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.5 });
    const frame = new THREE.Mesh(frameGeo, frameMat);
    frame.position.y = 4.2;
    signGroup.add(frame);

    // Dynamic Canvas Text
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
    const signPlane = new THREE.Mesh(new THREE.PlaneGeometry(9.6, 1.0), signPlaneMat);
    signPlane.position.set(0, 4.2, 0.2);
    signGroup.add(signPlane);

    // Support pillars
    const p1 = new THREE.Mesh(new THREE.BoxGeometry(0.3, 4.2, 0.3), frameMat);
    p1.position.set(-4.5, 2.1, 0);
    const p2 = new THREE.Mesh(new THREE.BoxGeometry(0.3, 4.2, 0.3), frameMat);
    p2.position.set(4.5, 2.1, 0);
    signGroup.add(p1); signGroup.add(p2);

    signGroup.position.set(-6, 0, -12);
    scene.add(signGroup);
}

function buildDebarkerStation() {
    const debarkerGroup = new THREE.Group();
    const hoodGeo = new THREE.BoxGeometry(2.4, 2.2, 2.4);
    const hoodMat = new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.6 });
    const hood = new THREE.Mesh(hoodGeo, hoodMat);
    hood.position.y = 1.3;
    hood.castShadow = true;
    debarkerGroup.add(hood);

    // Spinning Ribbed Rollers
    const rollerGeo = new THREE.CylinderGeometry(0.4, 0.4, 1.8, 12);
    const rollerMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.2, metalness: 0.7 });
    const r1 = new THREE.Mesh(rollerGeo, rollerMat);
    r1.rotation.x = Math.PI / 2;
    r1.position.set(-0.4, 1.4, 0);
    const r2 = new THREE.Mesh(rollerGeo, rollerMat);
    r2.rotation.x = Math.PI / 2;
    r2.position.set(0.4, 1.4, 0);
    debarkerGroup.userData = { r1, r2 };
    debarkerGroup.add(r1); debarkerGroup.add(r2);

    debarkerGroup.position.set(-11, 0, -12);
    scene.add(debarkerGroup);
}

function updateSaws3D() {
    sawMeshes.forEach(s => scene.remove(s));
    sawMeshes = [];

    const numSaws = Math.min(6, Math.max(1, gameState.upgrades.sawCount || 1));
    for (let i = 0; i < numSaws; i++) {
        const sawGroup = new THREE.Group();
        const archGeo = new THREE.BoxGeometry(0.4, 2.6, 2.4);
        const archMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.7 });
        const arch = new THREE.Mesh(archGeo, archMat);
        arch.position.y = 1.3;
        arch.castShadow = true;
        sawGroup.add(arch);

        // Flashing Warning Light on Top
        const lightGeo = new THREE.SphereGeometry(0.2, 8, 8);
        const lightMat = new THREE.MeshBasicMaterial({ color: 0xfacc15 });
        const light = new THREE.Mesh(lightGeo, lightMat);
        light.position.set(0, 2.7, 0);
        sawGroup.add(light);

        // Spinning Stainless Steel Blade
        const bladeGeo = new THREE.CylinderGeometry(0.95, 0.95, 0.06, 16);
        const bladeMat = new THREE.MeshStandardMaterial({ color: 0xe2e8f0, roughness: 0.2, metalness: 0.85 });
        const blade = new THREE.Mesh(bladeGeo, bladeMat);
        blade.rotation.x = Math.PI / 2;
        blade.position.y = 1.1;
        sawGroup.add(blade);

        sawGroup.position.set(-8 + (i * 1.5), 0, -12);
        sawGroup.userData = { blade, light };
        scene.add(sawGroup);
        sawMeshes.push(sawGroup);
    }
}

function buildAnimatedLumberjack() {
    lumberjackMesh = new THREE.Group();

    // Boots
    const bootGeo = new THREE.BoxGeometry(0.35, 0.35, 0.6);
    const bootMat = new THREE.MeshStandardMaterial({ color: 0x1e293b });
    const b1 = new THREE.Mesh(bootGeo, bootMat); b1.position.set(-0.25, 0.18, 0);
    const b2 = new THREE.Mesh(bootGeo, bootMat); b2.position.set(0.25, 0.18, 0);
    lumberjackMesh.add(b1); lumberjackMesh.add(b2);

    // Blue Denim Legs
    const legGeo = new THREE.BoxGeometry(0.3, 0.9, 0.3);
    const legMat = new THREE.MeshStandardMaterial({ color: 0x1d4ed8 });
    const l1 = new THREE.Mesh(legGeo, legMat); l1.position.set(-0.25, 0.7, 0);
    const l2 = new THREE.Mesh(legGeo, legMat); l2.position.set(0.25, 0.7, 0);
    lumberjackMesh.add(l1); lumberjackMesh.add(l2);

    // Red Flannel Torso
    const torsoGeo = new THREE.BoxGeometry(0.85, 1.1, 0.5);
    const torsoMat = new THREE.MeshStandardMaterial({ color: 0xdc2626 });
    const torso = new THREE.Mesh(torsoGeo, torsoMat);
    torso.position.y = 1.6;
    torso.castShadow = true;
    lumberjackMesh.add(torso);

    // Head
    const headGeo = new THREE.BoxGeometry(0.45, 0.45, 0.45);
    const headMat = new THREE.MeshStandardMaterial({ color: 0xfbcfe8 });
    const head = new THREE.Mesh(headGeo, headMat);
    head.position.y = 2.3;
    lumberjackMesh.add(head);

    // Yellow Safety Hardhat
    const hatGeo = new THREE.BoxGeometry(0.6, 0.25, 0.6);
    const hatMat = new THREE.MeshStandardMaterial({ color: 0xeab308 });
    const hat = new THREE.Mesh(hatGeo, hatMat);
    hat.position.y = 2.55;
    lumberjackMesh.add(hat);

    // Swinging Axe Arm
    const armGroup = new THREE.Group();
    const handleGeo = new THREE.CylinderGeometry(0.06, 0.06, 1.4, 6);
    const handleMat = new THREE.MeshStandardMaterial({ color: 0x78350f });
    const handle = new THREE.Mesh(handleGeo, handleMat);
    handle.position.y = -0.4;
    armGroup.add(handle);

    const bladeGeo = new THREE.BoxGeometry(0.1, 0.4, 0.5);
    const bladeMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, metalness: 0.8 });
    const blade = new THREE.Mesh(bladeGeo, bladeMat);
    blade.position.set(0, -0.9, 0.2);
    armGroup.add(blade);

    armGroup.position.set(0.5, 1.9, 0);
    lumberjackMesh.userData = { armGroup, swingTimer: 0 };
    lumberjackMesh.add(armGroup);

    lumberjackMesh.position.set(-30, 0, -20);
    scene.add(lumberjackMesh);
}

function buildGantryCrane() {
    gantryCraneGroup = new THREE.Group();

    // 4 Heavy Steel Legs
    const legGeo = new THREE.BoxGeometry(0.6, 7.5, 0.6);
    const craneMat = new THREE.MeshStandardMaterial({ color: 0xeab308, roughness: 0.4 });
    [[-6, -4], [6, -4], [-6, 4], [6, 4]].forEach(([lx, lz]) => {
        const leg = new THREE.Mesh(legGeo, craneMat);
        leg.position.set(lx, 3.75, lz);
        leg.castShadow = true;
        gantryCraneGroup.add(leg);
    });

    // Overhead Bridge Beam
    const beamGeo = new THREE.BoxGeometry(13.0, 0.8, 8.8);
    const beam = new THREE.Mesh(beamGeo, craneMat);
    beam.position.y = 7.4;
    beam.castShadow = true;
    gantryCraneGroup.add(beam);

    // Trolley & Red Spreader Hoist Block
    const trolleyGeo = new THREE.BoxGeometry(1.6, 0.6, 1.6);
    const trolleyMat = new THREE.MeshStandardMaterial({ color: 0x0f172a });
    const trolley = new THREE.Mesh(trolleyGeo, trolleyMat);
    trolley.position.y = 7.0;
    gantryCraneGroup.add(trolley);

    const hoistGeo = new THREE.BoxGeometry(2.4, 0.6, 1.4);
    const hoistMat = new THREE.MeshStandardMaterial({ color: 0xef4444 });
    const hoist = new THREE.Mesh(hoistGeo, hoistMat);
    hoist.position.y = 4.5;
    gantryCraneGroup.userData = { trolley, hoist, timer: 0 };
    gantryCraneGroup.add(hoist);

    gantryCraneGroup.position.set(-2, 0, 10);
    scene.add(gantryCraneGroup);
}

function buildAnimatedForklift() {
    forkliftMesh = new THREE.Group();

    // Yellow Chassis
    const bodyGeo = new THREE.BoxGeometry(1.8, 1.1, 2.6);
    const bodyMat = new THREE.MeshStandardMaterial({ color: 0xfacc15, roughness: 0.4 });
    const body = new THREE.Mesh(bodyGeo, bodyMat);
    body.position.y = 0.8;
    body.castShadow = true;
    forkliftMesh.add(body);

    // Roll Cage
    const cageGeo = new THREE.BoxGeometry(1.6, 1.4, 1.6);
    const cageMat = new THREE.MeshStandardMaterial({ color: 0x1e293b });
    const cage = new THREE.Mesh(cageGeo, cageMat);
    cage.position.set(0, 1.8, -0.2);
    forkliftMesh.add(cage);

    // Mast & Forks
    const mastGeo = new THREE.BoxGeometry(1.2, 2.2, 0.2);
    const mast = new THREE.Mesh(mastGeo, cageMat);
    mast.position.set(0, 1.4, 1.4);
    forkliftMesh.add(mast);

    const forkGeo = new THREE.BoxGeometry(1.4, 0.1, 1.2);
    const forkMat = new THREE.MeshStandardMaterial({ color: 0x475569 });
    const forks = new THREE.Mesh(forkGeo, forkMat);
    forks.position.set(0, 0.4, 1.8);
    forkliftMesh.userData = { forks, patrolProgress: 0 };
    forkliftMesh.add(forks);

    // 4 Wheels
    const wheelGeo = new THREE.CylinderGeometry(0.35, 0.35, 0.25, 12);
    const wheelMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.9 });
    [[-1.0, 0.35, 0.8], [1.0, 0.35, 0.8], [-1.0, 0.35, -0.8], [1.0, 0.35, -0.8]].forEach(([wx, wy, wz]) => {
        const wheel = new THREE.Mesh(wheelGeo, wheelMat);
        wheel.rotation.z = Math.PI / 2;
        wheel.position.set(wx, wy, wz);
        forkliftMesh.add(wheel);
    });

    forkliftMesh.position.set(4, 0, 8);
    scene.add(forkliftMesh);
}

function updateLumberTowers3D() {
    towerStackMeshes.forEach(m => scene.remove(m));
    towerStackMeshes = [];

    const tier = WOOD_TIERS[gameState.woodTier];
    const totalProcessed = gameState.stats.logsProcessed || 0;
    const layers = Math.min(28, Math.max(2, Math.floor(totalProcessed / 3) + 3));

    // Build 3 distinct stacks (Pine, Oak, Redwood)
    const stackOffsets = [[-4, 12], [0, 14], [-3, 18]];
    stackOffsets.forEach(([sx, sz], stackIdx) => {
        const stackColor = stackIdx === 0 ? tier.color : (stackIdx === 1 ? 0xd97706 : 0x991b1b);
        const stackLayers = Math.max(2, layers - stackIdx * 4);

        for (let l = 0; l < stackLayers; l++) {
            const plankGeo = new THREE.BoxGeometry(2.8, 0.22, 2.8);
            const plankMat = new THREE.MeshStandardMaterial({ color: stackColor, roughness: 0.7 });
            const plank = new THREE.Mesh(plankGeo, plankMat);
            plank.position.set(sx, 0.15 + l * 0.24, sz);
            plank.castShadow = true; plank.receiveShadow = true;
            scene.add(plank);
            towerStackMeshes.push(plank);
        }
    });
}

// ------------------------------------------
// 3D IN-WORLD UPGRADE PADS (Diegetic UI)
// ------------------------------------------
function buildWorldUpgradePads() {
    worldPadMeshes = [];
    WORLD_UPGRADE_PADS.forEach(pad => {
        const group = new THREE.Group();

        // 3D Beveled Box
        const padGeo = new THREE.BoxGeometry(3.6, 0.35, 2.6);
        const padMat = new THREE.MeshStandardMaterial({ color: 0x10b981, roughness: 0.4 });
        const padMesh = new THREE.Mesh(padGeo, padMat);
        padMesh.position.y = 0.17;
        padMesh.castShadow = true; padMesh.receiveShadow = true;
        group.add(padMesh);

        // Dynamic Canvas Label Texture
        const canvasTex = createPadTexture(pad);
        const tex = new THREE.CanvasTexture(canvasTex);
        const labelMat = new THREE.MeshBasicMaterial({ map: tex, transparent: true });
        const labelGeo = new THREE.PlaneGeometry(3.4, 2.4);
        const labelMesh = new THREE.Mesh(labelGeo, labelMat);
        labelMesh.rotation.x = -Math.PI / 2;
        labelMesh.position.y = 0.36;
        group.add(labelMesh);

        group.position.set(pad.pos[0], pad.pos[1], pad.pos[2]);
        group.userData = { pad, padMesh, labelMesh, tex, canvasTex };
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
    ctx.roundRect(8, 8, 240, 176, 20);
    ctx.fill();

    ctx.strokeStyle = canAfford ? "#6ee7b7" : "rgba(255,255,255,0.2)";
    ctx.lineWidth = canAfford ? 8 : 4;
    ctx.stroke();

    ctx.fillStyle = "#ffffff";
    ctx.font = "900 24px sans-serif";
    ctx.textAlign = "center";
    ctx.fillText(`${pad.icon} ${pad.label}`, 128, 65);

    ctx.fillStyle = canAfford ? "#fef08a" : "#94a3b8";
    ctx.font = "900 32px sans-serif";
    ctx.fillText(isMax ? 'MAX' : `💵 ${formatNumber(cost)}`, 128, 130);
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
// 3D DELIVERY TRUCK FLEET
// ------------------------------------------
class Truck3D {
    constructor(id) {
        this.id = id;
        this.state = "driving_in";
        this.cargo = 0;
        this.isJammed = false;
        this.z = -35 - id * 8.0;
        this.group = new THREE.Group();

        // Cab (Orange)
        const cabGeo = new THREE.BoxGeometry(2.0, 1.6, 2.4);
        const cabMat = new THREE.MeshStandardMaterial({ color: 0xea580c, roughness: 0.3 });
        const cab = new THREE.Mesh(cabGeo, cabMat);
        cab.position.set(0, 1.2, 1.0);
        cab.castShadow = true;
        this.group.add(cab);

        // Windshield
        const glassGeo = new THREE.BoxGeometry(1.8, 0.8, 0.2);
        const glassMat = new THREE.MeshStandardMaterial({ color: 0xe0f2fe, roughness: 0.1 });
        const glass = new THREE.Mesh(glassGeo, glassMat);
        glass.position.set(0, 1.4, 2.2);
        this.group.add(glass);

        // Flatbed (Slate Grey)
        const bedGeo = new THREE.BoxGeometry(2.2, 0.4, 3.8);
        const bedMat = new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.6 });
        const bed = new THREE.Mesh(bedGeo, bedMat);
        bed.position.set(0, 0.8, -1.8);
        bed.castShadow = true;
        this.group.add(bed);

        // 4 Wheels
        const wheelGeo = new THREE.CylinderGeometry(0.4, 0.4, 0.3, 12);
        const wheelMat = new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.9 });
        [[-1.1, 0.4, 1.0], [1.1, 0.4, 1.0], [-1.1, 0.4, -2.5], [1.1, 0.4, -2.5]].forEach(([wx, wy, wz]) => {
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
        this.emojiSprite.position.set(0, 3.4, 0);
        this.emojiSprite.visible = false;
        this.group.add(this.emojiSprite);

        this.group.position.set(18, 0, this.z);
        scene.add(this.group);
    }

    setEmoji(emoji) {
        if (!emoji) {
            this.emojiSprite.visible = false;
            return;
        }
        this.emojiCtx.clearRect(0, 0, 128, 128);
        this.emojiCtx.fillStyle = "#ffffff";
        this.emojiCtx.beginPath();
        this.emojiCtx.arc(64, 54, 48, 0, Math.PI * 2);
        this.emojiCtx.fill();
        this.emojiCtx.font = "54px sans-serif";
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
    overview: { cam: [0, 48, 48], look: [0, 0, 0] },
    forest:   { cam: [-36, 18, -14], look: [-35, 1, -22] },
    sawmill:  { cam: [-6, 16, -6], look: [-6, 2, -12] },
    yard:     { cam: [0, 22, 28], look: [0, 2, 14] },
    harbor:   { cam: [35, 18, 8], look: [26, 2, 8] },
    highway:  { cam: [18, 16, 2], look: [18, 2, 10] },
    hq:       { cam: [-28, 18, 22], look: [-34, 2, 24] }
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
            // Orbit / pan camera based on drag
            targetCamPos.x -= dx * 0.08;
            targetCamPos.z -= dy * 0.08;
            targetLookAt.x -= dx * 0.08;
            targetLookAt.z -= dy * 0.08;
        }
    });

    window.addEventListener("pointerup", () => {
        isDragging = false;
    });

    window.addEventListener("wheel", (e) => {
        targetCamPos.y = Math.max(12, Math.min(65, targetCamPos.y + e.deltaY * 0.03));
        targetCamPos.z = Math.max(15, Math.min(70, targetCamPos.z + e.deltaY * 0.03));
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

    // 1. Check Upgrade Pads
    for (const group of worldPadMeshes) {
        const hits = raycaster.intersectObjects(group.children, true);
        if (hits.length > 0) {
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
                truck.setEmoji("✨");
                gameState.stats.jamsCleared++;
                const bonus = 150 * (gameState.woodTier + 1);
                gameState.coins += bonus;
                gameState.totalEarned += bonus;
                audio.playSfx('cash');
                const screenP = toScreenXY(truck.group.position);
                floatingTexts2D.push(new FloatingText2D(screenP.x, screenP.y - 20, `+💵 ${bonus} UNJAMMED!`, "#34d399", 20));
                setTimeout(() => truck.setEmoji(null), 1200);
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
