import { describe, expect, it } from 'vitest';
import {
	angleDiff,
	BODY_VIEW_YAW,
	bodyYaw,
	eyeDistancePx,
	framing,
	type Landmark,
	LM,
	nearestBodyView,
	StillnessTracker
} from './pose-checks.ts';

/** A standing person facing the camera: head at `top`, feet at `bottom`, centred at `cx`. */
function person(top = 0.12, bottom = 0.92, cx = 0.5): Landmark[] {
	const lm: Landmark[] = Array.from({ length: 33 }, () => ({ x: cx, y: 0.5, z: 0, visibility: 0.99 }));
	const h = bottom - top;
	const at = (i: number, x: number, y: number) => (lm[i] = { x, y, z: 0, visibility: 0.99 });
	at(LM.nose, cx, top + 0.07 * h);
	at(LM.leftEye, cx + 0.01, top + 0.06 * h);
	at(LM.rightEye, cx - 0.01, top + 0.06 * h);
	at(LM.leftShoulder, cx + 0.06, top + 0.18 * h);
	at(LM.rightShoulder, cx - 0.06, top + 0.18 * h);
	at(LM.leftHip, cx + 0.04, top + 0.5 * h);
	at(LM.rightHip, cx - 0.04, top + 0.5 * h);
	at(LM.leftAnkle, cx + 0.03, bottom - 0.02);
	at(LM.rightAnkle, cx - 0.03, bottom - 0.02);
	at(LM.leftHeel, cx + 0.03, bottom);
	at(LM.rightHeel, cx - 0.03, bottom);
	return lm;
}

/** World landmarks for a body rotated by `yaw` degrees (+ = right side toward camera). */
function worldAt(yaw: number): Landmark[] {
	const rad = (yaw * Math.PI) / 180;
	const lm: Landmark[] = Array.from({ length: 33 }, () => ({ x: 0, y: 0, z: 0 }));
	// Facing camera: left shoulder at +x, nose at -z (toward camera). Rotate about the vertical axis.
	const rot = (x: number, z: number) => ({ x: x * Math.cos(rad) - z * Math.sin(rad) * -1, z: x * Math.sin(rad) + z * Math.cos(rad) });
	const set = (i: number, x: number, z: number) => (lm[i] = { ...rot(x, z), y: 0 });
	set(LM.leftShoulder, 0.2, 0);
	set(LM.rightShoulder, -0.2, 0);
	set(LM.nose, 0, -0.1);
	return lm;
}

describe('framing', () => {
	it('accepts a well-framed full body', () => {
		const f = framing(person());
		expect(f.hint).toBe('ok');
		expect(f.fullBodyVisible).toBe(true);
	});
	it('asks to step back when too large', () => expect(framing(person(0.01, 1.0)).hint).toBe('step_back'));
	it('asks to step closer when too small', () => expect(framing(person(0.4, 0.8)).hint).toBe('step_closer'));
	it('flags feet outside the frame', () => expect(framing(person(0.1, 0.995)).hint).toBe('feet_not_visible'));
	it('flags hidden feet (low visibility)', () => {
		const lm = person();
		for (const i of [LM.leftAnkle, LM.rightAnkle, LM.leftHeel, LM.rightHeel]) lm[i].visibility = 0.1;
		expect(framing(lm).hint).toBe('feet_not_visible');
	});
	it('asks to move toward the centre', () => {
		expect(framing(person(0.12, 0.92, 0.15)).hint).toBe('move_left');
		expect(framing(person(0.12, 0.92, 0.85)).hint).toBe('move_right');
	});
});

describe('bodyYaw', () => {
	it.each(Object.entries(BODY_VIEW_YAW))('recognises %s (%i°)', (view, yaw) => {
		const estimate = bodyYaw(worldAt(yaw));
		expect(angleDiff(estimate, yaw)).toBeLessThan(1);
		expect(nearestBodyView(estimate)).toBe(view);
	});
});

describe('angleDiff', () => {
	it('wraps around 180°', () => {
		expect(angleDiff(170, -170)).toBe(20);
		expect(angleDiff(0, 359)).toBe(1);
	});
});

describe('StillnessTracker', () => {
	it('becomes still only after holding for ~1 s', () => {
		const t = new StillnessTracker(1000, 0.01);
		const lm = person();
		expect(t.push(0, lm)).toBe(false);
		expect(t.push(500, lm)).toBe(false);
		expect(t.push(1000, lm)).toBe(true);
	});
	it('is not still while moving', () => {
		const t = new StillnessTracker(1000, 0.01);
		for (let ms = 0; ms <= 1200; ms += 100) {
			const moved = person(0.12 + ms / 20000, 0.92 + ms / 20000);
			expect(t.push(ms, moved)).toBe(false);
		}
	});
});

describe('eyeDistancePx', () => {
	it('measures the distance between the eyes in pixels', () => {
		expect(eyeDistancePx(person(), 1920, 1080)).toBeCloseTo(0.02 * 1920, 0);
	});
});
