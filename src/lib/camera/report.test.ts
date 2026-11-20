import { describe, expect, it } from 'vitest';
import { detectBrowser, f1Pass, pickBuiltInCamera, sanitizeTrackInfo } from './report.ts';

describe('detectBrowser', () => {
	it('tells Chrome and Safari apart on macOS', () => {
		const chrome =
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36';
		const safari =
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.1 Safari/605.1.15';
		expect(detectBrowser(chrome)).toBe('Chrome 142');
		expect(detectBrowser(safari)).toBe('Safari 26.1');
	});
});

describe('sanitizeTrackInfo', () => {
	it('removes device identifiers', () => {
		expect(sanitizeTrackInfo({ deviceId: 'abc', groupId: 'def', width: 1920 })).toEqual({ width: 1920 });
		expect(sanitizeTrackInfo(null)).toBeNull();
	});
});

describe('f1Pass', () => {
	it('passes at 720p or more, fails below, unknown without data', () => {
		expect(f1Pass([{ requested: '1080p', width: 1920, height: 1080 }])).toBe(true);
		expect(f1Pass([{ requested: '1080p', width: 640, height: 480 }])).toBe(false);
		expect(f1Pass([{ requested: '4K', error: 'OverconstrainedError' }])).toBeNull();
	});
});

describe('pickBuiltInCamera', () => {
	it('prefers the MacBook camera over others', () => {
		const devices = [{ label: 'iPhone Camera' }, { label: 'MacBook Pro Camera' }];
		expect(pickBuiltInCamera(devices)?.label).toBe('MacBook Pro Camera');
		expect(pickBuiltInCamera([{ label: 'USB Cam' }])?.label).toBe('USB Cam');
	});
});
