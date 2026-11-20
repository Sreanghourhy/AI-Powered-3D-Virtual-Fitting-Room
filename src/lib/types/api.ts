/** Types for FastAPI responses (JSON is camelCase). Backend: backend/app/api/schemas.py */

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
