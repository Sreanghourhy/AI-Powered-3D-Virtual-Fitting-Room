/**
 * Tiny per-browser flags (e.g. "privacy notice seen"). Storage can be unavailable
 * (private mode, blocked site data), so every access is guarded and falls back safely.
 */
export function getFlag(key: string, storage: Storage | undefined = globalThis.localStorage): boolean {
	try {
		return storage?.getItem(key) === '1';
	} catch {
		return false;
	}
}

export function setFlag(key: string, value: boolean, storage: Storage | undefined = globalThis.localStorage): void {
	try {
		if (value) storage?.setItem(key, '1');
		else storage?.removeItem(key);
	} catch {
		// Not critical: the notice will simply show again next time.
	}
}

export const PRIVACY_NOTICE_SEEN = 'fr.privacyNoticeSeen.v1';
