import { describe, expect, it } from 'vitest';
import { loginUrl, safeRedirect } from './redirect.ts';

describe('safeRedirect', () => {
	it('keeps local paths with query', () => {
		expect(safeRedirect('/try-on?top=shirt-oxford-blue')).toBe('/try-on?top=shirt-oxford-blue');
	});
	it.each([
		['https://evil.example/', 'absolute URL'],
		['//evil.example', 'protocol-relative'],
		['/\\evil.example', 'backslash trick'],
		['javascript:alert(1)', 'javascript URL'],
		['', 'empty'],
		[null, 'missing']
	])('rejects %s (%s)', (input, _reason) => {
		expect(safeRedirect(input, '/my-model')).toBe('/my-model');
	});
});

describe('loginUrl', () => {
	it('encodes the current path and query as redirectTo', () => {
		const url = new URL('http://localhost/try-on?top=shirt-oxford-blue');
		expect(loginUrl(url)).toBe('/login?redirectTo=%2Ftry-on%3Ftop%3Dshirt-oxford-blue');
		expect(safeRedirect(new URL(loginUrl(url), 'http://localhost').searchParams.get('redirectTo'))).toBe(
			'/try-on?top=shirt-oxford-blue'
		);
	});
});
