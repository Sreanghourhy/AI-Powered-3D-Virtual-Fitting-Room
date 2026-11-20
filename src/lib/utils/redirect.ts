/**
 * Only allow redirects to paths on this site (prevents open-redirect attacks via
 * ?redirectTo=https://evil.example or //evil.example).
 */
export function safeRedirect(target: string | null | undefined, fallback = '/'): string {
	if (!target || !target.startsWith('/') || target.startsWith('//') || target.startsWith('/\\')) {
		return fallback;
	}
	try {
		const url = new URL(target, 'http://local.invalid');
		if (url.origin !== 'http://local.invalid') return fallback;
		return `${url.pathname}${url.search}${url.hash}`;
	} catch {
		return fallback;
	}
}

/** URL of the login page that returns the user to `url` afterwards. */
export function loginUrl(url: URL): string {
	return `/login?redirectTo=${encodeURIComponent(`${url.pathname}${url.search}`)}`;
}
