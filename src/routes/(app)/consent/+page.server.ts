import { getConsentStatus } from '#lib/api/client.ts';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ fetch }) => ({
	consent: await getConsentStatus(fetch)
});
