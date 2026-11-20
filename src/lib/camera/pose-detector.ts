/**
 * MediaPipe Pose Landmarker in the browser, loaded ONLY from this app's own server
 * (static/mediapipe/, created by `npm run setup:mediapipe`). Browser-only: import lazily.
 */
import type { Landmark } from './pose-checks.ts';

export const MEDIAPIPE_WASM_PATH = '/mediapipe/wasm';
export const POSE_MODEL_PATH = '/mediapipe/models/pose_landmarker_full.task';

export interface PoseResult {
	/** One entry per detected person (max 2, to detect "more than one person"). */
	people: { landmarks: Landmark[]; world: Landmark[] }[];
}

export interface PoseDetector {
	detect(video: HTMLVideoElement, timestampMs: number): PoseResult;
	close(): void;
}

export class PoseModelMissingError extends Error {
	constructor() {
		super('MediaPipe files are missing. Run "npm run setup:mediapipe" and restart "npm run dev".');
		this.name = 'PoseModelMissingError';
	}
}

export async function createPoseDetector(): Promise<PoseDetector> {
	const probe = await fetch(POSE_MODEL_PATH, { method: 'HEAD' }).catch(() => null);
	if (!probe?.ok) throw new PoseModelMissingError();

	const { FilesetResolver, PoseLandmarker } = await import('@mediapipe/tasks-vision');
	const fileset = await FilesetResolver.forVisionTasks(MEDIAPIPE_WASM_PATH);
	const options = (delegate: 'GPU' | 'CPU') => ({
		baseOptions: { modelAssetPath: POSE_MODEL_PATH, delegate },
		runningMode: 'VIDEO' as const,
		numPoses: 2,
		minPoseDetectionConfidence: 0.5,
		minPosePresenceConfidence: 0.5,
		minTrackingConfidence: 0.5
	});
	let landmarker: Awaited<ReturnType<typeof PoseLandmarker.createFromOptions>>;
	try {
		landmarker = await PoseLandmarker.createFromOptions(fileset, options('GPU'));
	} catch {
		landmarker = await PoseLandmarker.createFromOptions(fileset, options('CPU')); // e.g. no WebGL
	}

	return {
		detect(video, timestampMs) {
			const r = landmarker.detectForVideo(video, timestampMs);
			return {
				people: r.landmarks.map((landmarks, i) => ({ landmarks, world: r.worldLandmarks[i] ?? [] }))
			};
		},
		close: () => landmarker.close()
	};
}
