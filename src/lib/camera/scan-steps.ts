/** The guided scan: 8 body views (turn 45° to your left each time) + 5 face close-ups. */
import type { BodyView } from './pose-checks.ts';

export type FaceView = 'face_front' | 'face_left_45' | 'face_right_45' | 'face_left_90' | 'face_right_90';
export type ScanView = BodyView | FaceView;

export interface ScanStep {
	view: ScanView;
	kind: 'body' | 'face';
	label: string;
	instruction: string;
}

export const SCAN_STEPS: ScanStep[] = [
	{ view: 'front', kind: 'body', label: 'Front', instruction: 'Face the screen' },
	{ view: 'front_right', kind: 'body', label: 'Front-right', instruction: 'Turn 45° to your left' },
	{ view: 'right', kind: 'body', label: 'Right side', instruction: 'Turn 45° more to your left (right side to the screen)' },
	{ view: 'back_right', kind: 'body', label: 'Back-right', instruction: 'Keep turning left, 45°' },
	{ view: 'back', kind: 'body', label: 'Back', instruction: 'Keep turning left: your back to the screen' },
	{ view: 'back_left', kind: 'body', label: 'Back-left', instruction: 'Keep turning left, 45°' },
	{ view: 'left', kind: 'body', label: 'Left side', instruction: 'Keep turning left (left side to the screen)' },
	{ view: 'front_left', kind: 'body', label: 'Front-left', instruction: 'Turn 45° more: almost facing the screen' },
	{ view: 'face_front', kind: 'face', label: 'Face', instruction: 'Come close (about 70 cm) and look at the camera' },
	{ view: 'face_left_45', kind: 'face', label: 'Face, left 45°', instruction: 'Turn your head a little to your left' },
	{ view: 'face_right_45', kind: 'face', label: 'Face, right 45°', instruction: 'Turn your head a little to your right' },
	{ view: 'face_left_90', kind: 'face', label: 'Face, left side', instruction: 'Turn your head fully to your left' },
	{ view: 'face_right_90', kind: 'face', label: 'Face, right side', instruction: 'Turn your head fully to your right' }
];

export const FRAMING_TEXT: Record<string, string> = {
	ok: 'Good, your whole body is in view',
	step_back: 'Step back a little',
	step_closer: 'Step a little closer',
	move_left: 'Move a little to your left',
	move_right: 'Move a little to your right',
	feet_not_visible: 'Your feet must be visible: step back or tilt the screen down',
	head_not_visible: 'Your head must be visible: step back or tilt the screen up'
};

export interface AutoCaptureState {
	phase: 'waiting' | 'countdown' | 'capture';
	/** Seconds left in the countdown (3, 2, 1). */
	remaining: number;
}

/**
 * Hands-free capture: when `ready` (in frame + still) a 3 s countdown runs, then "capture".
 * After a capture it is disarmed until the person has MOVED (turned), so one pose is
 * never captured twice. `trigger()` starts a manual countdown at any time (Space / button).
 */
export class AutoCapture {
	private countdownStart: number | null = null;
	private manual = false;
	private armed = true;

	constructor(private countdownMs = 3000) {}

	trigger(now: number): void {
		this.manual = true;
		this.countdownStart = now;
	}

	/** Call after a photo was taken (or when moving to another step). */
	reset(armed: boolean): void {
		this.countdownStart = null;
		this.manual = false;
		this.armed = armed;
	}

	update(now: number, input: { ready: boolean; moving: boolean }): AutoCaptureState {
		if (!this.armed && input.moving) this.armed = true;
		const allowed = this.manual || (this.armed && input.ready);
		if (!allowed) {
			this.countdownStart = null;
			return { phase: 'waiting', remaining: 0 };
		}
		this.countdownStart ??= now;
		const elapsed = now - this.countdownStart;
		if (elapsed >= this.countdownMs) {
			this.reset(false);
			return { phase: 'capture', remaining: 0 };
		}
		return { phase: 'countdown', remaining: Math.ceil((this.countdownMs - elapsed) / 1000) };
	}
}
