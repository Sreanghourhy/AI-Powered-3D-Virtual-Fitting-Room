import { getCurrentScan, listGarments } from '#lib/api/client.ts';
import { loadOrOffline } from '#lib/api/safe-load.ts';
import type { PageLoad } from './$types';

// Doesn't read url.search, so changing the outfit doesn't refetch the catalog.
export const load: PageLoad = async ({ fetch }) => {
	const [catalog, current] = await Promise.all([
		loadOrOffline(() => listGarments(undefined, fetch), []),
		loadOrOffline(() => getCurrentScan(fetch), null)
	]);
	return { garments: catalog.value, scan: current.value, backendError: catalog.backendError ?? current.backendError };
};
