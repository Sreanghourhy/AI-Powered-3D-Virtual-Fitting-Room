import { redirect } from '@sveltejs/kit';
import { getConsentStatus } from '#lib/api/client.ts';
import type { PageServerLoad } from './$types';

/** Capture requires the current consent version (docs/user-flows.md, Flow 1). */
export const load: PageServerLoad = async ({ fetch }) => {
	const consent = await getConsentStatus(fetch);
	if (!consent.accepted) redirect(303, '/consent');
	return {};
};
