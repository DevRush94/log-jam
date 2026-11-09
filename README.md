# Log Jam: Mill Empire

Canvas 2D isometric idle/tycoon web game + Python cloud save backend.

## Run Backend
```bash
python server.py
# -> Running at http://0.0.0.0:8000
```
Open `http://localhost:8000` or double click `index.html`.

## Features
- Single-file game (`index.html`) — zero external libraries, Web Audio chiptune/sfx synth.
- Full 8-station production line: Spawner -> Conveyor -> Saws -> Sorter -> Stacks -> Crane -> Docks -> Trucks.
- 13 upgrades, 5 wood tiers, prestige Golden Acorns, 17+ achievements, daily chest, offline earnings.
- Dual storage: local `localStorage` guest save + cloud sync (`/api/user/auth`, `/api/user/save`) matching Wings of Fire architecture.
