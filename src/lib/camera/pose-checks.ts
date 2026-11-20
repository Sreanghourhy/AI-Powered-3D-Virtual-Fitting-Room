/**
 * Pure helpers on MediaPipe Pose landmarks (33 points). No browser APIs, so they are unit-tested.
 *
 * Image landmarks: x, y normalised to [0, 1] (y down), visibility in [0, 1].
 * World landmarks: metres, origin at the hip centre, smaller z = closer to the camera.
 * Indices: https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker
 */

export interface Landmark {
	x: number;
	y: number;
	z: number;
	visibility?: number;
}

export const LM = {
	nose: 0,
	leftEye: 2,
	rightEye: 5,
	leftEar: 7,
	rightEar: 8,
	leftShoulder: 11,
	rightShoulder: 12,
	leftHip: 23,
	rightHip: 24,
	leftAnkle: 27,
	rightAnkle: 28,
	leftHeel: 29,
	rightHeel: 30
} as const;

/** Body views in capture order: turn 45° to your LEFT each time (yaw: + = right side toward camera). */
export const BODY_VIEW_YAW = {
	front: 0,
	front_right: 45,
	right: 90,
	back_right: 135,
	back: 180,
	back_left: -135,
	left: -90,
	front_left: -45
} as const;
export type BodyView = keyof typeof BODY_VIEW_YAW;
export const BODY_VIEW_ORDER = Object.keys(BODY_VIEW_YAW) as BodyView[];

const vis = (l: Landmark | undefined) => l?.visibility ?? 1;

// ---- Framing -----------------------------------------------------------------------

export interface Framing {
	/** Head top to feet, as a fraction of the image height. */
	heightFraction: number;
	headTop: number;
	feet: number;
	centerX: number;
	fullBodyVisible: boolean;
	hint: 'ok' | 'step_back' | 'step_closer' | 'move_left' | 'move_right' | 'feet_not_visible' | 'head_not_visible';
}

/**
 * Is the whole body (head to feet) inside the frame with a margin?
 * The head top isn't a landmark, so it is estimated above the nose from the nose–shoulder distance.
 * Directions in hints are for the person looking at a mirrored preview.
 */
export function framing(lm: Landmark[], margin = 0.03, minFraction = 0.55, maxFraction = 0.94): Framing {
	const shoulderY = (lm[LM.leftShoulder].y + lm[LM.rightShoulder].y) / 2;
	const nose = lm[LM.nose];
	const headTop = nose.y - Math.max(0.6 * (shoulderY - nose.y), 0.02);
	const feetPoints = [LM.leftAnkle, LM.rightAnkle, LM.leftHeel, LM.rightHeel].map((i) => lm[i]);
	const feet = Math.max(...feetPoints.map((p) => p.y));
	const feetSeen = feetPoints.some((p) => vis(p) > 0.3);
	const centerX = (lm[LM.leftHip].x + lm[LM.rightHip].x) / 2;
	const heightFraction = feet - headTop;

	let hint: Framing['hint'] = 'ok';
	if (headTop < margin) hint = heightFraction > maxFraction ? 'step_back' : 'head_not_visible';
	else if (feet > 1 - margin || !feetSeen) hint = heightFraction > maxFraction ? 'step_back' : 'feet_not_visible';
	else if (heightFraction > maxFraction) hint = 'step_back';
	else if (heightFraction < minFraction) hint = 'step_closer';
	// Preview is mirrored: the person sees themselves on the other side.
	else if (centerX < 0.3) hint = 'move_left';
	else if (centerX > 0.7) hint = 'move_right';

	return { heightFraction, headTop, feet, centerX, fullBodyVisible: hint === 'ok', hint };
}

// ---- Facing direction ----------------------------------------------------------------

/**
 * Body yaw in degrees from world landmarks: 0 = facing the camera, 90 = right side toward
 * the camera, ±180 = back, -90 = left side. Shoulders give the angle; the nose being in front of
 * or behind the shoulders decides front vs back. This is a HINT only (accuracy is being measured).
 */
export function bodyYaw(world: Landmark[]): number {
	const l = world[LM.leftShoulder];
	const r = world[LM.rightShoulder];
	const dx = l.x - r.x;
	const dz = l.z - r.z;
	const side = (Math.atan2(dz, Math.abs(dx)) * 180) / Math.PI; // -90..90
	const shoulderZ = (l.z + r.z) / 2;
	const facingCamera = world[LM.nose].z < shoulderZ;
	if (facingCamera) return side;
	return side >= 0 ? 180 - side : -180 - side;
}

/** Smallest difference between two angles, in degrees (0..180). */
export function angleDiff(a: number, b: number): number {
	const d = Math.abs((((a - b) % 360) + 540) % 360 - 180);
	return d;
}

export function nearestBodyView(yaw: number): BodyView {
	return BODY_VIEW_ORDER.reduce((best, v) => (angleDiff(yaw, BODY_VIEW_YAW[v]) < angleDiff(yaw, BODY_VIEW_YAW[best]) ? v : best));
}

// ---- Stillness -------------------------------------------------------------------------

const STILL_POINTS = [LM.nose, LM.leftShoulder, LM.rightShoulder, LM.leftHip, LM.rightHip, LM.leftAnkle, LM.rightAnkle];

/** True once key points have moved less than `tolerance` (fraction of image) for `holdMs`. */
export class StillnessTracker {
	private history: { t: number; pts: { x: number; y: number }[] }[] = [];

	constructor(
		private holdMs = 1000,
		private tolerance = 0.012
	) {}

	reset(): void {
		this.history = [];
	}

	push(t: number, lm: Landmark[]): boolean {
		this.history.push({ t, pts: STILL_POINTS.map((i) => ({ x: lm[i].x, y: lm[i].y })) });
		while (this.history.length > 1 && t - this.history[0].t > this.holdMs * 1.5) this.history.shift();
		const window = this.history.filter((h) => t - h.t <= this.holdMs);
		if (window.length < 3 || t - window[0].t < this.holdMs * 0.8) return false;
		const first = window[0].pts;
		return window.every((h) => h.pts.every((p, i) => Math.hypot(p.x - first[i].x, p.y - first[i].y) < this.tolerance));
	}
}

// ---- Face close-ups -------------------------------------------------------------------

/** Distance between the eyes in pixels (face close-up detail, target ≥ 100 px). */
export function eyeDistancePx(lm: Landmark[], width: number, height: number): number {
	const a = lm[LM.leftEye];
	const b = lm[LM.rightEye];
	return Math.hypot((a.x - b.x) * width, (a.y - b.y) * height);
}
