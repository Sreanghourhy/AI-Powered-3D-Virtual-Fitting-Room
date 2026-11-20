import { isRedirect } from '@sveltejs/kit';
import { describe, expect, it } from 'vitest';

// All route files, by path (keys only; nothing is executed).
const routeFiles = Object.keys(import.meta.glob('/src/routes/**/+*.{svelte,ts}'));

// Raw source of every frontend file, for guard checks.
const sources = import.meta.glob('/src/**/*.{svelte,ts}', { query: '?raw', import: 'default', eager: true }) as Record<
	string,
	string
>;

describe('single-user app (CR-02)', () => {
	it('TC-01: has no login, sign-up, profile or consent routes', () => {
		const forbidden = /\/(login|signup|sign-up|register|account|profile|consent)(\/|$)/;
		expect(routeFiles.filter((f) => forbidden.test(f.replace(/\/\+[^/]+$/, '')))).toEqual([]);
	});

	it('TC-01: the fitting room is the root page', () => {
		expect(routeFiles).toContain('/src/routes/+page.svelte');
		expect(routeFiles).toContain('/src/routes/scan/+page.svelte');
	});

	it('TC-55: the public sample model is only used by the dev viewer demo (no avatar fallback)', () => {
		const users = Object.entries(sources)
			.filter(([path, code]) => code.includes('sample.glb') && !path.endsWith('.test.ts'))
			.map(([path]) => path);
		expect(users).toEqual(['/src/routes/viewer-demo/+page.svelte']);
	});
});

describe('dev-only routes', () => {
	it('every /dev page is blocked in production by a server load (404)', () => {
		const devPages = routeFiles.filter((f) => f.startsWith('/src/routes/dev/') && f.endsWith('/+page.svelte'));
		expect(devPages.length).toBeGreaterThan(0);
		for (const pagePath of devPages) {
			const guard = sources[pagePath.replace('+page.svelte', '+page.server.ts')];
			expect(guard, `${pagePath} needs a +page.server.ts guard`).toMatch(/if \(!dev\) error\(404/);
		}
	});
});

describe('TC-02: old routes redirect', () => {
	const call = async (path: string, url: string) => {
		const { load } = await import(/* @vite-ignore */ path);
		try {
			load({ url: new URL(url) });
		} catch (e) {
			if (isRedirect(e)) return { status: e.status, location: e.location };
			throw e;
		}
		throw new Error('expected a redirect');
	};

	it('/try-on keeps the outfit and goes to /', async () => {
		expect(await call('./try-on/+page.server.ts', 'http://localhost/try-on?top=a&bottom=b')).toEqual({
			status: 307,
			location: '/?top=a&bottom=b'
		});
	});
	it('/my-model goes to /', async () => {
		expect(await call('./my-model/+page.server.ts', 'http://localhost/my-model')).toEqual({ status: 307, location: '/' });
	});
	it('/capture goes to /scan', async () => {
		expect(await call('./capture/+page.server.ts', 'http://localhost/capture')).toEqual({ status: 307, location: '/scan' });
	});
});
