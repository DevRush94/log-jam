const fs = require('fs');

const html = fs.readFileSync('index.html', 'utf8');
const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/);
if (!scriptMatch) {
    console.error("No script tag found!");
    process.exit(1);
}
const js = scriptMatch[1];

// Mock basic DOM
global.window = {
    innerWidth: 1920,
    innerHeight: 1080,
    devicePixelRatio: 1,
    addEventListener: (ev, fn) => {
        if (ev === 'DOMContentLoaded') setTimeout(fn, 10);
    }
};
global.document = {
    createElement: (tag) => ({
        getContext: () => ({
            clearRect: () => {},
            beginPath: () => {},
            arc: () => {},
            fill: () => {},
            stroke: () => {},
            fillText: () => {},
            fillRect: () => {},
            roundRect: () => {},
            resetTransform: () => {},
            scale: () => {}
        }),
        width: 100,
        height: 100,
        style: {}
    }),
    getElementById: (id) => ({
        getContext: () => ({
            clearRect: () => {},
            beginPath: () => {},
            arc: () => {},
            fill: () => {},
            stroke: () => {},
            fillText: () => {},
            fillRect: () => {},
            roundRect: () => {},
            resetTransform: () => {},
            scale: () => {}
        }),
        classList: { add: () => {}, remove: () => {} },
        style: {},
        appendChild: () => {},
        innerHTML: ""
    }),
    querySelectorAll: () => []
};
global.localStorage = {
    getItem: () => null,
    setItem: () => {}
};
global.performance = { now: () => 1000 };
global.requestAnimationFrame = (fn) => {};

// Mock THREE.js
global.THREE = {
    Scene: class {
        constructor() { this.children = []; }
        add(obj) { this.children.push(obj); }
        remove(obj) {}
    },
    Color: class {},
    FogExp2: class {},
    PerspectiveCamera: class {
        constructor() {
            this.position = { set: () => {}, lerp: () => {} };
        }
        lookAt() {}
        updateProjectionMatrix() {}
    },
    WebGLRenderer: class {
        constructor() {
            this.domElement = { getBoundingClientRect: () => ({ left: 0, top: 0, width: 1920, height: 1080 }) };
            this.shadowMap = {};
        }
        setSize() {}
        setPixelRatio() {}
    },
    HemisphereLight: class { constructor() {} },
    DirectionalLight: class {
        constructor() {
            this.position = { set: () => {} };
            this.shadow = { mapSize: {}, camera: {} };
        }
    },
    BoxGeometry: class {},
    MeshStandardMaterial: class {
        constructor() {
            this.color = { setHex: () => {} };
        }
    },
    MeshBasicMaterial: class {},
    Mesh: class {
        constructor() {
            this.position = { set: () => {}, clone: () => ({ project: () => ({ x: 0, y: 0 }) }) };
            this.rotation = { set: () => {} };
            this.scale = { set: () => {} };
            this.material = { color: { setHex: () => {} } };
        }
    },
    PlaneGeometry: class {},
    CylinderGeometry: class {},
    Group: class {
        constructor() {
            this.children = [];
            this.position = { set: () => {} };
            this.rotation = { set: () => {} };
        }
        add(obj) { this.children.push(obj); }
    },
    ConeGeometry: class {},
    SphereGeometry: class {},
    RingGeometry: class {},
    CanvasTexture: class { constructor() {} },
    SpriteMaterial: class {},
    Sprite: class {
        constructor() {
            this.scale = { set: () => {} };
            this.position = { set: () => {} };
        }
    },
    Vector2: class { constructor() {} },
    Vector3: class {
        constructor(x, y, z) { this.x = x || 0; this.y = y || 0; this.z = z || 0; }
        set(x, y, z) { this.x = x; this.y = y; this.z = z; }
        lerp() {}
        clone() { return this; }
        project() { return this; }
    },
    Raycaster: class {
        constructor() {
            this.setFromCamera = () => {};
            this.intersectObjects = () => [];
        }
    },
    PCFSoftShadowMap: 1,
    DoubleSide: 2
};

try {
    eval(js);
    console.log("EVAL SUCCESS! Script executed without errors.");
} catch (err) {
    console.error("EVAL ERROR:", err);
}
