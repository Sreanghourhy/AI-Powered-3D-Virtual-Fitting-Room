import { listGarments } from '#lib/api/client.ts';
import { parseCategory } from '#lib/components/garments/categories.ts';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, url }) => {
	const category = parseCategory(url.searchParams.get('category'));
	return { category, garments: await listGarments(category, fetch) };
};
