import { describe, expect, it } from 'vitest';
import { rewriteApiUrl } from './api-proxy.ts';

const APP = 'http://localhost:5173';
const API = 'http://127.0.0.1:8000';

describe('rewriteApiUrl', () => {
	it('maps /api/* to the backend and keeps the query', () => {
		expect(rewriteApiUrl(`${APP}/api/garments?category=top`, APP, API)).toBe(`${API}/garments?category=top`);
	});
	it('ignores non-api paths', () => {
		expect(rewriteApiUrl(`${APP}/catalog`, APP, API)).toBeNull();
		expect(rewriteApiUrl(`${APP}/apiary`, APP, API)).toBeNull();
	});
	it('never rewrites other origins (no cookie leak to third parties)', () => {
		expect(rewriteApiUrl('https://evil.example/api/auth/me', APP, API)).toBeNull();
	});
});
