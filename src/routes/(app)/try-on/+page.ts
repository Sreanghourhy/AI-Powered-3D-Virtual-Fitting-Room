import { listGarments } from '#lib/api/client.ts';
import type { PageLoad } from './$types';

// Doesn't read url.search, so changing the outfit doesn't refetch the catalog.
export const load: PageLoad = async ({ fetch }) => ({ garments: await listGarments(undefined, fetch) });
