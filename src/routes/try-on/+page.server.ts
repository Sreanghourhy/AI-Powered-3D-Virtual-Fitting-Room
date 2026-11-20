import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';

/** Old route (merged into the fitting room, CR-02). Keeps ?top=&bottom=. */
export const load: PageServerLoad = ({ url }) => redirect(307, `/${url.search}`);
