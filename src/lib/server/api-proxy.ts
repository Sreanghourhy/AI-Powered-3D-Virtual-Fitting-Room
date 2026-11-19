/** Helpers for reaching FastAPI during server-side rendering. */

export const SESSION_COOKIE = 'fr_session';

/**
 * If `requestUrl` targets this app's /api/*, return the matching backend URL.
 * Otherwise return null (leave the request untouched).
 */
export function rewriteApiUrl(requestUrl: string, appOrigin: string, backend: string): string | null {
	const url = new URL(requestUrl);
	if (url.origin !== appOrigin) return null;
	if (url.pathname !== '/api' && !url.pathname.startsWith('/api/')) return null;
	return `${backend}${url.pathname.slice('/api'.length) || '/'}${url.search}`;
}
