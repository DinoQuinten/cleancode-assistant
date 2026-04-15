# Excalidraw JSON Schema

Reference: https://github.com/excalidraw/excalidraw/tree/master/packages/excalidraw/data

Excalidraw is a free collaborative whiteboard. Its scene format is plain JSON that can be hand-authored or generated.

## Scene top-level

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "system-and-database-design plugin",
  "elements": [ /* ... */ ],
  "appState": {
    "viewBackgroundColor": "#ffffff",
    "gridSize": 20
  },
  "files": {}
}
```

## Element types

Common: `rectangle`, `ellipse`, `diamond`, `arrow`, `line`, `text`.

### Rectangle (a service, component, box)

```json
{
  "id": "svc-api",
  "type": "rectangle",
  "x": 100,
  "y": 100,
  "width": 180,
  "height": 80,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "#a5d8ff",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "roundness": { "type": 3 },
  "seed": 1,
  "version": 1,
  "versionNonce": 1,
  "isDeleted": false,
  "boundElements": [],
  "updated": 0,
  "link": null,
  "locked": false
}
```

### Text (label on a shape)

```json
{
  "id": "text-api",
  "type": "text",
  "x": 150,
  "y": 130,
  "width": 80,
  "height": 20,
  "text": "API",
  "fontSize": 20,
  "fontFamily": 1,
  "textAlign": "center",
  "verticalAlign": "middle",
  "containerId": "svc-api",
  "originalText": "API",
  "lineHeight": 1.25,
  "baseline": 18,
  "seed": 2,
  "version": 1,
  "versionNonce": 2,
  "isDeleted": false
}
```

Set `containerId` to attach the text to a shape; shape's `boundElements` includes `{ "id": "<text-id>", "type": "text" }`.

### Arrow (connection)

```json
{
  "id": "arrow-1",
  "type": "arrow",
  "x": 280,
  "y": 140,
  "width": 100,
  "height": 0,
  "points": [[0, 0], [100, 0]],
  "startBinding": { "elementId": "svc-api", "focus": 0, "gap": 1 },
  "endBinding":   { "elementId": "svc-db",  "focus": 0, "gap": 1 },
  "startArrowhead": null,
  "endArrowhead": "arrow",
  "strokeColor": "#1e1e1e",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "seed": 3,
  "version": 1,
  "versionNonce": 3,
  "isDeleted": false
}
```

The `elementId` in `startBinding`/`endBinding` MUST reference an existing element `id`.

## Color palette (pleasant defaults)

| Role | bgColor |
|---|---|
| Client / user | `#fff3bf` (yellow) |
| Edge / gateway | `#ffe8cc` (orange) |
| Service | `#a5d8ff` (blue) |
| Database / storage | `#d0bfff` (purple) |
| Queue / stream | `#b2f2bb` (green) |
| External system | `#e9ecef` (gray) |
| Caution / hot path | `#ffc9c9` (red) |

Stroke `#1e1e1e` for all.

## Layout heuristics (when generating)

- Grid size: 20 px
- Box size: 180 × 80 for services, 200 × 60 for databases
- Horizontal spacing: 120 px
- Vertical spacing: 100 px
- Left-to-right request flow; top-to-bottom hierarchies
- Start top-left at (100, 100)

## Importing

In Excalidraw: **File → Open** → pick the `.excalidraw` file, OR paste JSON via **Ctrl+Shift+V** into an empty canvas.

## Minimal valid scene

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "generated",
  "elements": [
    {
      "id": "hello",
      "type": "rectangle",
      "x": 100, "y": 100, "width": 120, "height": 60,
      "strokeColor": "#1e1e1e", "backgroundColor": "#a5d8ff",
      "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
      "roughness": 1, "opacity": 100, "seed": 1, "version": 1,
      "versionNonce": 1, "isDeleted": false,
      "boundElements": [], "updated": 0, "link": null, "locked": false,
      "roundness": { "type": 3 }, "angle": 0
    }
  ],
  "appState": { "viewBackgroundColor": "#ffffff", "gridSize": 20 },
  "files": {}
}
```

## Gotchas

- Every `id` must be unique; reuse breaks bindings silently
- `boundElements` on the shape and `containerId` on the text must both exist for the label to follow the shape on move
- `strokeColor` and `backgroundColor` don't have alpha; use `opacity` (0-100)
- Roughness: 0 = clean, 1 = default Excalidraw sketchy, 2 = very rough
- Arrow `points` are relative to the arrow's `x,y`; first point is always `[0, 0]`
