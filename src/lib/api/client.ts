/**
 * Typed client for the FastAPI backend.
 *
 * Always call paths under /api. In the browser, Vite proxies /api to FastAPI (dev).
 * During server-side rendering, the handleFetch hook (src/hooks.server.ts) rewrites
 * /api to the backend URL and forwards the session cookie. Pass SvelteKit's `fetch`
 * from load functions so that works.
 */
import type { Garment, GarmentCategory } from '#lib/types/garment.ts';
import type { ConsentStatus, Consent, HealthResponse, Job, User } from '#lib/types/api.ts';

export const API_BASE = '/api';

/** Required by the backend on every state-changing request (localhost protection, D10). */
export const WRITE_HEADER = 'X-Fitting-Room';

type Fetch = typeof fetch;

export class ApiError extends Error {
	constructor(
		public readonly status: number,
		message: string
	) {
		super(message);
		this.name = 'ApiError';
	}
}

/** Turn a FastAPI error body into one readable sentence. */
export function errorMessage(status: number, body: unknown): string {
	if (body && typeof body === 'object' && 'detail' in body) {
		const detail = (body as { detail: unknown }).detail;
		if (typeof detail === 'string') return detail;
		if (Array.isArray(detail) && detail.length > 0) {
			// Pydantic validation errors: [{loc: [...], msg: "..."}]
			const first = detail[0] as { loc?: unknown[]; msg?: string };
			const field = first.loc?.at(-1);
			const msg = (first.msg ?? 'Invalid value').replace(/^Value error, /, '');
			return typeof field === 'string' ? `${field}: ${msg}` : msg;
		}
	}
	if (status === 0) return 'Cannot reach the server. Check your connection.';
	if (status >= 500) return 'Something went wrong on our side. Please try again.';
	return `Request failed (${status})`;
}

export async function apiFetch<T>(path: string, init: RequestInit = {}, fetchFn: Fetch = fetch): Promise<T> {
	const headers = new Headers(init.headers);
	headers.set('Accept', 'application/json');
	headers.set(WRITE_HEADER, '1');
	if (init.body !== undefined && !(init.body instanceof FormData)) {
		headers.set('Content-Type', 'application/json');
	}

	let response: Response;
	try {
		response = await fetchFn(`${API_BASE}${path}`, { credentials: 'include', ...init, headers });
	} catch {
		throw new ApiError(0, errorMessage(0, null));
	}

	if (!response.ok) {
		const body = await response.json().catch(() => null);
		throw new ApiError(response.status, errorMessage(response.status, body));
	}
	if (response.status === 204) return undefined as T;
	return (await response.json()) as T;
}

const json = (body: unknown) => JSON.stringify(body);

// ---- Health -------------------------------------------------------------------
export const getHealth = (f?: Fetch) => apiFetch<HealthResponse>('/health', {}, f);

// ---- Auth ---------------------------------------------------------------------
export interface Credentials {
	email: string;
	password: string;
}
export const signup = (c: Credentials, f?: Fetch) =>
	apiFetch<User>('/auth/signup', { method: 'POST', body: json(c) }, f);
export const login = (c: Credentials, f?: Fetch) =>
	apiFetch<User>('/auth/login', { method: 'POST', body: json(c) }, f);
export const logout = (f?: Fetch) => apiFetch<void>('/auth/logout', { method: 'POST' }, f);
export const getMe = (f?: Fetch) => apiFetch<User>('/auth/me', {}, f);

// ---- Consent ------------------------------------------------------------------
export const getConsentStatus = (f?: Fetch) => apiFetch<ConsentStatus>('/consents/me', {}, f);
export const acceptConsent = (version: string, f?: Fetch) =>
	apiFetch<Consent>(
		'/consents',
		{
			method: 'POST',
			body: json({ version, confirmsAdultAndSelf: true, agreesToCaptureAndStorage: true })
		},
		f
	);
export const withdrawConsent = (id: string, f?: Fetch) =>
	apiFetch<void>(`/consents/${encodeURIComponent(id)}`, { method: 'DELETE' }, f);

// ---- Catalog ------------------------------------------------------------------
export const listGarments = (category?: GarmentCategory, f?: Fetch) =>
	apiFetch<Garment[]>(category ? `/garments?category=${category}` : '/garments', {}, f);
export const getGarment = (id: string, f?: Fetch) =>
	apiFetch<Garment>(`/garments/${encodeURIComponent(id)}`, {}, f);

// ---- Jobs ---------------------------------------------------------------------
export const getJob = (id: string, f?: Fetch) => apiFetch<Job>(`/jobs/${encodeURIComponent(id)}`, {}, f);
