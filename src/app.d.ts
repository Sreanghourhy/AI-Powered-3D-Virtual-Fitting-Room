// See https://svelte.dev/docs/kit/types#app.d.ts
// Single-user local prototype (CR-02): no auth, so no user in App.Locals.
declare global {
	namespace App {
		// interface Error {}
		// interface Locals {}
		// interface PageData {}
		// interface PageState {}
		// interface Platform {}
	}
}

export {};
