import { describe, expect, it, vi } from 'vitest';
import type { Scan } from '#lib/types/api.ts';
import { saveScan, type SaveDeps } from './save-scan.ts';

const scan = (status: Scan['status']): Scan => ({
	id: 's1',
	status,
	createdAt: '',
	completedAt: null,
	images: [],
	missingViews: []
});

function deps(overrides: Partial<SaveDeps> = {}): SaveDeps {
	return {
		createScan: vi.fn().mockResolvedValue(scan('capturing')),
		uploadScanImage: vi.fn().mockResolvedValue(scan('capturing')),
		completeScan: vi.fn().mockResolvedValue(scan('saved')),
		...overrides
	};
}

const photos = [
	{ view: 'front', blob: new Blob(['a']) },
	{ view: 'back', blob: new Blob(['b']) }
];

describe('saveScan', () => {
	it('creates, uploads every photo with its view, completes, and reports progress', async () => {
		const d = deps();
		const progress: string[] = [];
		const result = await saveScan(photos, (done, total) => progress.push(`${done}/${total}`), d, 0);
		expect(result.status).toBe('saved');
		expect(d.uploadScanImage).toHaveBeenNthCalledWith(1, 's1', 'front', photos[0].blob);
		expect(d.uploadScanImage).toHaveBeenNthCalledWith(2, 's1', 'back', photos[1].blob);
		expect(d.completeScan).toHaveBeenCalledWith('s1');
		expect(progress).toEqual(['0/2', '1/2', '2/2']);
	});

	it('retries a failed upload', async () => {
		const upload = vi.fn().mockRejectedValueOnce(new Error('network')).mockResolvedValue(scan('capturing'));
		const d = deps({ uploadScanImage: upload });
		await saveScan(photos, undefined, d, 1);
		expect(upload).toHaveBeenCalledTimes(3);
	});

	it('gives up after the retries and does not complete', async () => {
		const d = deps({ uploadScanImage: vi.fn().mockRejectedValue(new Error('down')) });
		await expect(saveScan(photos, undefined, d, 1)).rejects.toThrow('down');
		expect(d.completeScan).not.toHaveBeenCalled();
	});
});
