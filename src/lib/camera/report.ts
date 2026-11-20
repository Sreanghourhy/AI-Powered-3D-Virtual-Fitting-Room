/** Camera capability report for the feasibility tests (P3-01). Contains no images. */

export const RESOLUTION_LADDER = [
	{ label: '4K', width: 3840, height: 2160 },
	{ label: '1440p', width: 2560, height: 1440 },
	{ label: '1080p', width: 1920, height: 1080 },
	{ label: '720p', width: 1280, height: 720 }
] as const;

export interface LadderResult {
	requested: string;
	width?: number;
	height?: number;
	frameRate?: number;
	error?: string;
}

export interface StillResult {
	method: 'canvas' | 'ImageCapture.takePhoto';
	width?: number;
	height?: number;
	sharpness?: number;
	jpegBytes?: number;
	error?: string;
}

export interface CameraReport {
	tool: 'camera-lab P3-01';
	generatedAt: string;
	browser: string;
	userAgent: string;
	cameras: string[];
	selectedCamera: string;
	supportedConstraints: string[];
	settings: Record<string, unknown>;
	capabilities: Record<string, unknown> | null;
	measuredFps: number | null;
	ladder: LadderResult[];
	stills: StillResult[];
	f1Pass: boolean | null;
}

export function detectBrowser(ua: string): string {
	const version = (re: RegExp) => ua.match(re)?.[1] ?? '?';
	if (/Edg\//.test(ua)) return `Edge ${version(/Edg\/(\d+)/)}`;
	if (/Firefox\//.test(ua)) return `Firefox ${version(/Firefox\/(\d+)/)}`;
	if (/Chrome\//.test(ua)) return `Chrome ${version(/Chrome\/(\d+)/)}`;
	if (/Safari\//.test(ua)) return `Safari ${version(/Version\/(\d+(?:\.\d+)?)/)}`;
	return 'Other';
}

/** Drop per-site device identifiers before a report leaves the page. */
export function sanitizeTrackInfo<T extends object>(info: T | null | undefined): Record<string, unknown> | null {
	if (!info) return null;
	const out: Record<string, unknown> = {};
	for (const [key, value] of Object.entries(info)) {
		if (key === 'deviceId' || key === 'groupId') continue;
		out[key] = value;
	}
	return out;
}

/** F1 (feasibility): browser must deliver at least 1280×720 from the built-in camera. */
export function f1Pass(ladder: LadderResult[]): boolean | null {
	const delivered = ladder.filter((r) => r.width && r.height);
	if (delivered.length === 0) return null;
	return delivered.some((r) => r.width! >= 1280 && r.height! >= 720);
}

/** Built-in MacBook camera first, so it is the default choice. */
export function pickBuiltInCamera<T extends { label: string }>(devices: T[]): T | undefined {
	return devices.find((d) => /macbook|facetime|built-?in/i.test(d.label)) ?? devices[0];
}
