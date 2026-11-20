import { redirect } from '@sveltejs/kit';
import { loginUrl } from '#lib/utils/redirect.ts';
import type { LayoutServerLoad } from './$types';

/** Every page in the (app) group requires a signed-in user. */
export const load: LayoutServerLoad = ({ locals, url }) => {
	if (!locals.user) redirect(303, loginUrl(url));
	return { user: locals.user };
};
