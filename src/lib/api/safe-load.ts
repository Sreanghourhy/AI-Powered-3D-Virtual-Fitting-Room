import { ApiError } from './client.ts';

/** Message shown when the local FastAPI backend isn't running. */
export const BACKEND_OFFLINE =
	'The backend is not running. Start it in a terminal with: npm run dev:api (then reload this page).';

/**
 * Run a loader request; if the backend is down (no connection or 5xx from the dev proxy),
 * return `fallback` plus a readable message instead of crashing the page with a 500.
 * Other errors (e.g. 404, 422) are real bugs and are re-thrown.
 */
export async function loadOrOffline<T>(
	request: () => Promise<T>,
	fallback: T
): Promise<{ value: T; backendError: string | null }> {
	try {
		return { value: await request(), backendError: null };
	} catch (e) {
		if (e instanceof ApiError && (e.status === 0 || e.status >= 500)) {
			return { value: fallback, backendError: BACKEND_OFFLINE };
		}
		throw e;
	}
}
