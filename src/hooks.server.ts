import type { HandleFetch } from '@sveltejs/kit/hooks';
import { API_URL } from '$app/env/private';
import { rewriteApiUrl, SESSION_COOKIE } from '#lib/server/api-proxy.ts';

/** During SSR, send /api/* straight to FastAPI and forward only the session cookie. */
export const handleFetch: HandleFetch = async ({ event, request, fetch }) => {
	const target = rewriteApiUrl(request.url, event.url.origin, API_URL);
	if (!target) return fetch(request);

	const headers = new Headers(request.headers);
	headers.delete('cookie');
	const token = event.cookies.get(SESSION_COOKIE);
	if (token) headers.set('cookie', `${SESSION_COOKIE}=${token}`);

	const init: RequestInit & { duplex?: 'half' } = { method: request.method, headers };
	if (request.body) {
		init.body = request.body;
		init.duplex = 'half';
	}
	return fetch(new Request(target, init));
};
