/** Types for FastAPI responses (JSON is camelCase). Backend: backend/app/api/schemas.py */

export interface User {
	id: string;
	email: string;
	createdAt: string;
}

export interface Consent {
	id: string;
	version: string;
	scope: string;
	grantedAt: string;
	withdrawnAt: string | null;
}

export interface ConsentStatus {
	requiredVersion: string;
	accepted: boolean;
	consents: Consent[];
}

export type JobStatus = 'queued' | 'processing' | 'done' | 'failed';

export interface Job {
	id: string;
	type: string;
	status: JobStatus;
	progress: number;
	step: string | null;
	/** Customer-safe message when status is "failed". */
	error: string | null;
	createdAt: string;
	startedAt: string | null;
	finishedAt: string | null;
}

export interface HealthResponse {
	status: 'ok';
}
