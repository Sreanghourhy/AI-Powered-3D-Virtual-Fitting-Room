import type { HandleFetch } from '@sveltejs/kit/hooks';
import { API_URL } from '$app/env/private';
import { rewriteApiUrl } from '#lib/server/api-proxy.ts';

/** During SSR, send /api/* straight to the local FastAPI backend (no cookies: no auth, CR-02). */
export const handleFetch: HandleFetch = async ({ event, request, fetch }) => {
	const target = rewriteApiUrl(request.url, event.url.origin, API_URL);
	if (!target) return fetch(request);

	const headers = new Headers(request.headers);
	headers.delete('cookie');

	const init: RequestInit & { duplex?: 'half' } = { method: request.method, headers };
	if (request.body) {
		init.body = request.body;
		init.duplex = 'half';
	}
	return fetch(new Request(target, init));
};
