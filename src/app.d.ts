// See https://svelte.dev/docs/kit/types#app.d.ts
import type { User } from '#lib/types/api.ts';

declare global {
	namespace App {
		// interface Error {}
		interface Locals {
			/** Signed-in user, resolved once per request in hooks.server.ts. */
			user: User | null;
		}
		// interface PageData {}
		// interface PageState {}
		// interface Platform {}
	}
}

export {};
