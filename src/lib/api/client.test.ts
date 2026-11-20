import { describe, expect, it, vi } from 'vitest';
import { ApiError, apiFetch, errorMessage, listGarments } from './client.ts';

const jsonResponse = (status: number, body: unknown) =>
	new Response(body === undefined ? null : JSON.stringify(body), {
		status,
		headers: { 'Content-Type': 'application/json' }
	});

describe('errorMessage', () => {
	it('uses FastAPI string detail', () => {
		expect(errorMessage(401, { detail: 'Email or password is wrong' })).toBe('Email or password is wrong');
	});
	it('summarises the first validation error with its field', () => {
		const body = { detail: [{ loc: ['body', 'password'], msg: 'String should have at least 10 characters' }] };
		expect(errorMessage(422, body)).toBe('password: String should have at least 10 characters');
	});
	it('hides server internals on 5xx', () => {
		expect(errorMessage(500, null)).toBe('Something went wrong on our side. Please try again.');
	});
});

describe('apiFetch', () => {
	it('prefixes /api, sends credentials and JSON headers', async () => {
		const fetchFn = vi.fn().mockResolvedValue(jsonResponse(200, { ok: true }));
		await apiFetch('/auth/login', { method: 'POST', body: '{}' }, fetchFn);
		const [url, init] = fetchFn.mock.calls[0];
		expect(url).toBe('/api/auth/login');
		expect(init.credentials).toBe('include');
		expect(new Headers(init.headers).get('Content-Type')).toBe('application/json');
		expect(new Headers(init.headers).get('X-Fitting-Room')).toBe('1');
	});

	it('returns undefined for 204', async () => {
		const fetchFn = vi.fn().mockResolvedValue(new Response(null, { status: 204 }));
		await expect(apiFetch('/auth/logout', { method: 'POST' }, fetchFn)).resolves.toBeUndefined();
	});

	it('throws ApiError with status and readable message', async () => {
		const fetchFn = vi.fn().mockResolvedValue(jsonResponse(409, { detail: 'An account with this email already exists' }));
		const error = (await apiFetch('/auth/signup', {}, fetchFn).catch((e: unknown) => e)) as ApiError;
		expect(error).toBeInstanceOf(ApiError);
		expect(error.status).toBe(409);
		expect(error.message).toBe('An account with this email already exists');
	});

	it('maps network failure to status 0', async () => {
		const fetchFn = vi.fn().mockRejectedValue(new TypeError('Failed to fetch'));
		const error = (await apiFetch('/health', {}, fetchFn).catch((e: unknown) => e)) as ApiError;
		expect(error.status).toBe(0);
	});

	it('builds the catalog category query', async () => {
		const fetchFn = vi.fn().mockResolvedValue(jsonResponse(200, []));
		await listGarments('bottom', fetchFn);
		expect(fetchFn.mock.calls[0][0]).toBe('/api/garments?category=bottom');
	});
});
