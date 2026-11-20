/**
 * What the fitting-room stage shows. There is deliberately no "sample/avatar" state:
 * if no real model of the person exists, the stage stays empty (FR-07, CR-02).
 */
export type ModelState =
	| { kind: 'none' }
	| { kind: 'generating'; progress: number; step: string | null }
	| { kind: 'ready'; modelUrl: string }
	| { kind: 'failed'; reason: string };
