import { defineEnvVars } from '@sveltejs/kit/env';

/** Environment variables (SvelteKit 3). Private unless `public: true`. */
export const variables = defineEnvVars({
	API_URL: {
		description: 'FastAPI backend URL used during server-side rendering (server-only).',
		schema: (value) => (value || 'http://127.0.0.1:8000').replace(/\/$/, '')
	}
});
