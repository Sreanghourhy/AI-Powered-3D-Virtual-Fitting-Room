import { describe, expect, it } from 'vitest';
import { ApiError } from './client.ts';
import { BACKEND_OFFLINE, loadOrOffline } from './safe-load.ts';

describe('loadOrOffline', () => {
	it('returns the value when the backend answers', async () => {
		expect(await loadOrOffline(async () => [1, 2], [])).toEqual({ value: [1, 2], backendError: null });
	});

	it.each([0, 500, 502, 503])('falls back with a clear message when the backend is down (status %i)', async (status) => {
		const result = await loadOrOffline(async () => {
			throw new ApiError(status, 'down');
		}, []);
		expect(result).toEqual({ value: [], backendError: BACKEND_OFFLINE });
	});

	it('re-throws real API errors', async () => {
		await expect(
			loadOrOffline(async () => {
				throw new ApiError(422, 'bad category');
			}, [])
		).rejects.toThrow('bad category');
	});
});
