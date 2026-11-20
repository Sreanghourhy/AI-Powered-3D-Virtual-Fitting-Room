import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

/** Old route (merged into the fitting room, CR-02). */
export const load: PageServerLoad = () => redirect(307, '/');
