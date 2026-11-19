/** Thin typed wrapper around fetch for the FastAPI backend (proxied at /api in dev). */

const API_BASE = '/api';

export class ApiError extends Error {
	constructor(
		public status: number,
		message: string
	) {
		super(message);
		this.name = 'ApiError';
	}
}

export async function apiFetch<T>(
	path: string,
	init: RequestInit = {},
	fetchFn: typeof fetch = fetch
): Promise<T> {
	const response = await fetchFn(`${API_BASE}${path}`, {
		credentials: 'include',
		...init,
		headers: { Accept: 'application/json', ...init.headers }
	});

	if (!response.ok) {
		throw new ApiError(response.status, `${init.method ?? 'GET'} ${path} failed (${response.status})`);
	}
	return (await response.json()) as T;
}

export interface HealthResponse {
	status: 'ok';
}

export const getHealth = (fetchFn?: typeof fetch) => apiFetch<HealthResponse>('/health', {}, fetchFn);
