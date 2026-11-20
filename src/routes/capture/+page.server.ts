import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

/** Old route (renamed to /scan, CR-02). */
export const load: PageServerLoad = () => redirect(307, '/scan');
