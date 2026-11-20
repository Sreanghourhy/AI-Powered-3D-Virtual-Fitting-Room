import { describe, expect, it } from 'vitest';
import { safeRedirect } from './redirect.ts';

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
