/**
 * Image sharpness = variance of the 4-neighbour Laplacian on grayscale pixels.
 * Higher = sharper. Same metric the backend blur check will use (P3-09), so numbers compare.
 */

/** RGBA bytes → luminance (Rec. 601), one value per pixel. */
export function toGrayscale(rgba: Uint8ClampedArray): Float32Array {
	const gray = new Float32Array(rgba.length / 4);
	for (let i = 0, p = 0; i < gray.length; i++, p += 4) {
		gray[i] = 0.299 * rgba[p] + 0.587 * rgba[p + 1] + 0.114 * rgba[p + 2];
	}
	return gray;
}

export function laplacianVariance(gray: ArrayLike<number>, width: number, height: number): number {
	if (width < 3 || height < 3) return 0;
	let sum = 0;
	let sumSq = 0;
	let n = 0;
	for (let y = 1; y < height - 1; y++) {
		const row = y * width;
		for (let x = 1; x < width - 1; x++) {
			const i = row + x;
			const lap = gray[i - 1] + gray[i + 1] + gray[i - width] + gray[i + width] - 4 * gray[i];
			sum += lap;
			sumSq += lap * lap;
			n++;
		}
	}
	const mean = sum / n;
	return sumSq / n - mean * mean;
}

export function sharpnessOf(image: { data: Uint8ClampedArray; width: number; height: number }): number {
	return laplacianVariance(toGrayscale(image.data), image.width, image.height);
}
