import type { Handle, HandleFetch } from '@sveltejs/kit/hooks';
import { API_URL } from '$app/env/private';
import { rewriteApiUrl, SESSION_COOKIE } from '#lib/server/api-proxy.ts';
import type { User } from '#lib/types/api.ts';

/** Resolve the signed-in user (if any) once per request. */
export const handle: Handle = async ({ event, resolve }) => {
	event.locals.user = null;
	if (event.cookies.get(SESSION_COOKIE)) {
		try {
			const response = await event.fetch('/api/auth/me');
			if (response.ok) event.locals.user = (await response.json()) as User;
		} catch {
			// Backend unreachable: treat as signed out rather than failing the page.
		}
	}
	return resolve(event);
};

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
