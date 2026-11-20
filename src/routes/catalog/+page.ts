import { listGarments } from '#lib/api/client.ts';
import { loadOrOffline } from '#lib/api/safe-load.ts';
import { parseCategory } from '#lib/components/garments/categories.ts';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, url }) => {
	const category = parseCategory(url.searchParams.get('category'));
	const { value: garments, backendError } = await loadOrOffline(() => listGarments(category, fetch), []);
	return { category, garments, backendError };
};
