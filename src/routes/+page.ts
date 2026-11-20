import { listGarments } from '#lib/api/client.ts';
import { loadOrOffline } from '#lib/api/safe-load.ts';
import type { PageLoad } from './$types';

// Doesn't read url.search, so changing the outfit doesn't refetch the catalog.
export const load: PageLoad = async ({ fetch }) => {
	const { value: garments, backendError } = await loadOrOffline(() => listGarments(undefined, fetch), []);
	return { garments, backendError };
};
