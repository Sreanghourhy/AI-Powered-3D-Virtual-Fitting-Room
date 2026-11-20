/** Thin wrappers around the browser camera APIs (MediaDevices / getUserMedia). */
import { sharpnessOf } from './sharpness.ts';
import type { StillResult } from './report.ts';

export function stopStream(stream: MediaStream | null | undefined): void {
	stream?.getTracks().forEach((track) => track.stop());
}

export function openCamera(opts: { deviceId?: string; width: number; height: number; frameRate?: number }): Promise<MediaStream> {
	return navigator.mediaDevices.getUserMedia({
		audio: false,
		video: {
			deviceId: opts.deviceId ? { exact: opts.deviceId } : undefined,
			width: { ideal: opts.width },
			height: { ideal: opts.height },
			frameRate: { ideal: opts.frameRate ?? 30 }
		}
	});
}

export async function listCameras(): Promise<MediaDeviceInfo[]> {
	return (await navigator.mediaDevices.enumerateDevices()).filter((d) => d.kind === 'videoinput');
}

/** Count real decoded frames for `ms` milliseconds. */
export function measureFps(video: HTMLVideoElement, ms = 3000): Promise<number | null> {
	type RVFC = (cb: () => void) => number;
	const rvfc = (video as HTMLVideoElement & { requestVideoFrameCallback?: RVFC }).requestVideoFrameCallback;
	if (!rvfc) return Promise.resolve(null);
	return new Promise((resolve) => {
		let frames = 0;
		const start = performance.now();
		const tick = () => {
			frames++;
			if (performance.now() - start < ms) rvfc.call(video, tick);
			else resolve(Math.round((frames * 10000) / (performance.now() - start)) / 10);
		};
		rvfc.call(video, tick);
	});
}

function toJpegBytes(canvas: HTMLCanvasElement): Promise<number> {
	return new Promise((resolve) => canvas.toBlob((b) => resolve(b?.size ?? 0), 'image/jpeg', 0.92));
}

/** Full-resolution frame from the live video (unmirrored). */
export async function grabCanvasStill(video: HTMLVideoElement): Promise<{ result: StillResult; canvas: HTMLCanvasElement }> {
	const canvas = document.createElement('canvas');
	canvas.width = video.videoWidth;
	canvas.height = video.videoHeight;
	const ctx = canvas.getContext('2d', { willReadFrequently: true })!;
	ctx.drawImage(video, 0, 0);
	const image = ctx.getImageData(0, 0, canvas.width, canvas.height);
	return {
		canvas,
		result: {
			method: 'canvas',
			width: canvas.width,
			height: canvas.height,
			sharpness: Math.round(sharpnessOf(image)),
			jpegBytes: await toJpegBytes(canvas)
		}
	};
}

/** ImageCapture.takePhoto() where the browser supports it (Chrome yes, Safari usually no). */
export async function takePhotoStill(track: MediaStreamTrack): Promise<StillResult> {
	const ImageCaptureCtor = (globalThis as { ImageCapture?: new (t: MediaStreamTrack) => { takePhoto(): Promise<Blob> } })
		.ImageCapture;
	if (!ImageCaptureCtor) return { method: 'ImageCapture.takePhoto', error: 'Not supported in this browser' };
	try {
		const blob = await new ImageCaptureCtor(track).takePhoto();
		const bitmap = await createImageBitmap(blob);
		const canvas = document.createElement('canvas');
		canvas.width = bitmap.width;
		canvas.height = bitmap.height;
		const ctx = canvas.getContext('2d', { willReadFrequently: true })!;
		ctx.drawImage(bitmap, 0, 0);
		const image = ctx.getImageData(0, 0, canvas.width, canvas.height);
		return {
			method: 'ImageCapture.takePhoto',
			width: bitmap.width,
			height: bitmap.height,
			sharpness: Math.round(sharpnessOf(image)),
			jpegBytes: blob.size
		};
	} catch (e) {
		return { method: 'ImageCapture.takePhoto', error: e instanceof Error ? `${e.name}: ${e.message}` : String(e) };
	}
}
