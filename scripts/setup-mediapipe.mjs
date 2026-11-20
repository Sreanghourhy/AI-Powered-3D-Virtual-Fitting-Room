#!/usr/bin/env node
// Self-host MediaPipe so the browser never calls a third party while the camera is on.
// Copies the WASM runtime from node_modules and downloads the pose model once.
// Output (git-ignored): static/mediapipe/wasm/*, static/mediapipe/models/pose_landmarker_full.task
import { createHash } from 'node:crypto';
import { copyFileSync, existsSync, mkdirSync, readFileSync, renameSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const out = join(root, 'static', 'mediapipe');
const wasmSrc = join(root, 'node_modules', '@mediapipe', 'tasks-vision', 'wasm');

// Pinned model version (Apache-2.0, Google MediaPipe "Pose Landmarker (Full)").
const MODEL_URL =
	'https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_full/float16/1/pose_landmarker_full.task';
const MODEL_SHA256 = '5134a3aad27a58b93da0088d431f366da362b44e3ccfbe3462b3827a839011b1';
const MODEL_FILE = join(out, 'models', 'pose_landmarker_full.task');

mkdirSync(join(out, 'wasm'), { recursive: true });
mkdirSync(join(out, 'models'), { recursive: true });

for (const file of ['vision_wasm_internal.js', 'vision_wasm_internal.wasm']) {
	copyFileSync(join(wasmSrc, file), join(out, 'wasm', file));
}
console.log('MediaPipe WASM copied to static/mediapipe/wasm/');

// The exact file is pinned by its SHA-256, so a changed or corrupted download is rejected.
const looksValid = (path) => existsSync(path) && createHash('sha256').update(readFileSync(path)).digest('hex') === MODEL_SHA256;

if (looksValid(MODEL_FILE)) {
	console.log('Pose model already present.');
} else {
	console.log('Downloading pose model (~9 MB)…');
	const response = await fetch(MODEL_URL);
	if (!response.ok) throw new Error(`Model download failed: HTTP ${response.status}`);
	const tmp = `${MODEL_FILE}.download`;
	writeFileSync(tmp, Buffer.from(await response.arrayBuffer()));
	if (!looksValid(tmp)) throw new Error('Downloaded model does not match the pinned SHA-256');
	renameSync(tmp, MODEL_FILE);
	console.log('Pose model saved to static/mediapipe/models/');
}
