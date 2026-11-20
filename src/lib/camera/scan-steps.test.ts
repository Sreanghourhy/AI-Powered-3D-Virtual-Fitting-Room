import { describe, expect, it } from 'vitest';
import { AutoCapture, SCAN_STEPS } from './scan-steps.ts';

describe('SCAN_STEPS', () => {
	it('has 8 body views then 5 face views, matching the backend names', () => {
		expect(SCAN_STEPS.filter((s) => s.kind === 'body')).toHaveLength(8);
		expect(SCAN_STEPS.filter((s) => s.kind === 'face')).toHaveLength(5);
		expect(SCAN_STEPS.map((s) => s.view)).toEqual([
			'front', 'front_right', 'right', 'back_right', 'back', 'back_left', 'left', 'front_left',
			'face_front', 'face_left_45', 'face_right_45', 'face_left_90', 'face_right_90'
		]);
	});
});

describe('AutoCapture', () => {
	it('counts down 3-2-1 while ready, then captures', () => {
		const a = new AutoCapture(3000);
		const ready = { ready: true, moving: false };
		expect(a.update(0, ready)).toEqual({ phase: 'countdown', remaining: 3 });
		expect(a.update(1500, ready).remaining).toBe(2);
		expect(a.update(2500, ready).remaining).toBe(1);
		expect(a.update(3000, ready).phase).toBe('capture');
	});

	it('cancels the countdown when the person is no longer ready', () => {
		const a = new AutoCapture(3000);
		a.update(0, { ready: true, moving: false });
		expect(a.update(1000, { ready: false, moving: true }).phase).toBe('waiting');
		expect(a.update(1100, { ready: true, moving: false })).toEqual({ phase: 'countdown', remaining: 3 });
	});

	it('does not capture the same pose twice: needs movement first', () => {
		const a = new AutoCapture(1000);
		const still = { ready: true, moving: false };
		a.update(0, still);
		expect(a.update(1000, still).phase).toBe('capture');
		expect(a.update(1100, still).phase).toBe('waiting'); // still standing the same way
		expect(a.update(5000, still).phase).toBe('waiting');
		a.update(5100, { ready: false, moving: true }); // turned
		expect(a.update(5200, still).phase).toBe('countdown');
	});

	it('manual trigger counts down even when not ready', () => {
		const a = new AutoCapture(3000);
		a.reset(false);
		a.trigger(0);
		expect(a.update(100, { ready: false, moving: false }).phase).toBe('countdown');
		expect(a.update(3000, { ready: false, moving: false }).phase).toBe('capture');
	});
});
