import { error } from '@sveltejs/kit';
import { dev } from '$app/env';
import type { PageServerLoad } from './$types';

/** Feasibility lab (Phase 3, P3-01..P3-05). Development only: 404 in production builds. */
export const load: PageServerLoad = () => {
	if (!dev) error(404, 'Not found');
};
