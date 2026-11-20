/** Upload a finished capture: create scan → upload each photo (with retries) → complete. */
import { completeScan, createScan, uploadScanImage } from '#lib/api/client.ts';
import type { Scan } from '#lib/types/api.ts';

export interface PhotoToSave {
	view: string;
	blob: Blob;
}

export interface SaveDeps {
	createScan: typeof createScan;
	uploadScanImage: typeof uploadScanImage;
	completeScan: typeof completeScan;
}

const realDeps: SaveDeps = { createScan, uploadScanImage, completeScan };

export async function saveScan(
	photos: PhotoToSave[],
	onprogress: (done: number, total: number) => void = () => {},
	deps: SaveDeps = realDeps,
	retries = 2
): Promise<Scan> {
	const scan = await deps.createScan();
	onprogress(0, photos.length);
	for (const [i, photo] of photos.entries()) {
		for (let attempt = 0; ; attempt++) {
			try {
				await deps.uploadScanImage(scan.id, photo.view, photo.blob);
				break;
			} catch (e) {
				if (attempt >= retries) throw e;
				await new Promise((r) => setTimeout(r, 300 * (attempt + 1)));
			}
		}
		onprogress(i + 1, photos.length);
	}
	return deps.completeScan(scan.id);
}
