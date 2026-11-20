import { describe, expect, it } from 'vitest';
import { laplacianVariance, sharpnessOf, toGrayscale } from './sharpness.ts';

function rgbaFromGray(gray: number[]): Uint8ClampedArray {
	const out = new Uint8ClampedArray(gray.length * 4);
	gray.forEach((v, i) => out.set([v, v, v, 255], i * 4));
	return out;
}

describe('sharpness', () => {
	it('converts RGBA to luminance', () => {
		expect(Array.from(toGrayscale(new Uint8ClampedArray([255, 255, 255, 255, 0, 0, 0, 255])))).toEqual([
			expect.closeTo(255, 3),
			0
		]);
	});

	it('is zero for a flat image', () => {
		expect(laplacianVariance(new Array(25).fill(128), 5, 5)).toBe(0);
	});

	it('is higher for a sharp checkerboard than for a soft gradient', () => {
		const w = 16;
		const checker = Array.from({ length: w * w }, (_, i) => ((i % w) + Math.floor(i / w)) % 2 ? 255 : 0);
		const gradient = Array.from({ length: w * w }, (_, i) => (i % w) * 16);
		const sharp = sharpnessOf({ data: rgbaFromGray(checker), width: w, height: w });
		const soft = sharpnessOf({ data: rgbaFromGray(gradient), width: w, height: w });
		expect(sharp).toBeGreaterThan(soft * 100);
	});

	it('handles images too small to measure', () => {
		expect(laplacianVariance([1, 2, 3, 4], 2, 2)).toBe(0);
	});
});
