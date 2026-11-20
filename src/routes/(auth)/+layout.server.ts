import { redirect } from '@sveltejs/kit';
import { safeRedirect } from '#lib/utils/redirect.ts';
import type { LayoutServerLoad } from './$types';

/** Login and sign-up are for signed-out visitors only. */
export const load: LayoutServerLoad = ({ locals, url }) => {
	if (locals.user) redirect(303, safeRedirect(url.searchParams.get('redirectTo'), '/my-model'));
};
