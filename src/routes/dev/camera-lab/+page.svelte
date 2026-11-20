<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	import { page } from '$app/state';
	import { grabCanvasStill, listCameras, measureFps, openCamera, stopStream, takePhotoStill } from '#lib/camera/media.ts';
	import {
		type CameraReport,
		detectBrowser,
		f1Pass,
		type LadderResult,
		pickBuiltInCamera,
		RESOLUTION_LADDER,
		sanitizeTrackInfo,
		type StillResult
	} from '#lib/camera/report.ts';

	// P3-01 camera capability probe. Runs only in this browser and sends nothing to any server.

	let video: HTMLVideoElement | undefined = $state();
	let stream: MediaStream | null = null;
	let running = $state(false);
	let cameraOn = $state(false);
	let log = $state<string[]>([]);
	let report = $state<CameraReport | null>(null);
	let previewUrl = $state<string | null>(null);
	let errorText = $state<string | null>(null);

	const say = (line: string) => (log = [...log, line]);

	async function attach(s: MediaStream) {
		stopStream(stream);
		stream = s;
		cameraOn = true;
		if (!video) return;
		video.srcObject = s;
		await video.play();
		// Wait until real frames arrive so videoWidth/Height are valid.
		if (!video.videoWidth) await new Promise((r) => video!.addEventListener('loadedmetadata', r, { once: true }));
	}

	function stopCamera() {
		stopStream(stream);
		stream = null;
		cameraOn = false;
		if (video) video.srcObject = null;
	}

	async function run() {
		running = true;
		errorText = null;
		log = [];
		report = null;
		try {
			say('Requesting camera permission…');
			await attach(await openCamera({ width: 1920, height: 1080 }));

			const cameras = await listCameras(); // labels are available after permission
			const chosen = pickBuiltInCamera(cameras);
			say(`Cameras found: ${cameras.map((c) => c.label || '(no label)').join(', ') || 'none'}`);
			if (chosen && stream!.getVideoTracks()[0].getSettings().deviceId !== chosen.deviceId) {
				say(`Switching to ${chosen.label}`);
				await attach(await openCamera({ deviceId: chosen.deviceId, width: 1920, height: 1080 }));
			}
			const deviceId = chosen?.deviceId;

			const ladder: LadderResult[] = [];
			for (const step of RESOLUTION_LADDER) {
				say(`Requesting ${step.label} (${step.width}×${step.height})…`);
				try {
					await attach(await openCamera({ deviceId, width: step.width, height: step.height }));
					const s = stream!.getVideoTracks()[0].getSettings();
					ladder.push({ requested: step.label, width: s.width, height: s.height, frameRate: s.frameRate });
					say(`  → delivered ${s.width}×${s.height} @ ${s.frameRate ?? '?'} fps`);
				} catch (e) {
					const message = e instanceof Error ? `${e.name}: ${e.message}` : String(e);
					ladder.push({ requested: step.label, error: message });
					say(`  → failed: ${message}`);
				}
			}

			// Measure on the best mode the camera delivered.
			const best = ladder.filter((r) => r.width).sort((a, b) => b.width! * b.height! - a.width! * a.height!)[0];
			say(`Using best mode ${best ? `${best.width}×${best.height}` : '(default)'} for measurements…`);
			await attach(await openCamera({ deviceId, width: best?.width ?? 1920, height: best?.height ?? 1080 }));
			const track = stream!.getVideoTracks()[0];

			say('Measuring real frame rate for 3 s…');
			const fps = await measureFps(video!, 3000);

			say('Capturing a still from the video (canvas)…');
			const stills: StillResult[] = [];
			const canvasStill = await grabCanvasStill(video!);
			stills.push(canvasStill.result);
			previewUrl = canvasStill.canvas.toDataURL('image/jpeg', 0.6);

			say('Trying ImageCapture.takePhoto()…');
			stills.push(await takePhotoStill(track));

			report = {
				tool: 'camera-lab P3-01',
				generatedAt: new Date().toISOString(),
				browser: detectBrowser(navigator.userAgent),
				userAgent: navigator.userAgent,
				cameras: cameras.map((c) => c.label || '(no label)'),
				selectedCamera: track.label,
				supportedConstraints: Object.entries(navigator.mediaDevices.getSupportedConstraints())
					.filter(([, v]) => v)
					.map(([k]) => k)
					.sort(),
				settings: sanitizeTrackInfo(track.getSettings()) ?? {},
				capabilities: sanitizeTrackInfo(track.getCapabilities?.()),
				measuredFps: fps,
				ladder,
				stills,
				f1Pass: f1Pass(ladder)
			};
			say('Done. The camera is now off.');
		} catch (e) {
			errorText =
				e instanceof DOMException && e.name === 'NotAllowedError'
					? 'Camera access was blocked. Allow it in the browser (address bar) and in System Settings → Privacy & Security → Camera, then try again.'
					: e instanceof Error
						? `${e.name}: ${e.message}`
						: String(e);
		} finally {
			stopCamera(); // privacy: never leave the camera running after the probe
			running = false;
		}
	}

	let copyState = $state<'idle' | 'copied' | 'failed'>('idle');

	function download() {
		if (!report) return;
		const name = `camera-report-${report.browser.split(' ')[0].toLowerCase()}.json`;
		const url = URL.createObjectURL(new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' }));
		// The link must be in the document, and the URL must outlive the click:
		// revoking it immediately cancels the download in Safari.
		const a = Object.assign(document.createElement('a'), { href: url, download: name });
		document.body.append(a);
		a.click();
		a.remove();
		setTimeout(() => URL.revokeObjectURL(url), 60_000);
	}

	async function copyReport() {
		if (!report) return;
		try {
			await navigator.clipboard.writeText(JSON.stringify(report, null, 2));
			copyState = 'copied';
		} catch {
			copyState = 'failed';
		}
	}

	// ?autorun=1 starts the probe on load (used for automated checks with a fake camera).
	onMount(() => {
		if (page.url.searchParams.get('autorun') === '1') run();
	});

	// Camera off when leaving the page, closing the tab or hiding the page.
	onDestroy(stopCamera);
	$effect(() => {
		const off = () => stopCamera();
		window.addEventListener('pagehide', off);
		return () => window.removeEventListener('pagehide', off);
	});

	const capabilityKeys = ['width', 'height', 'frameRate', 'aspectRatio', 'facingMode', 'resizeMode', 'exposureMode', 'exposureCompensation', 'exposureTime', 'whiteBalanceMode', 'colorTemperature', 'focusMode', 'focusDistance', 'zoom', 'brightness', 'contrast', 'saturation', 'sharpness'];
	const show = (v: unknown) => (v === undefined ? '—' : typeof v === 'object' ? JSON.stringify(v) : String(v));
</script>

<svelte:head><title>Camera lab (dev) · Fitting Room</title></svelte:head>

<main class="mx-auto max-w-6xl px-4 py-8 sm:px-6">
	<p class="text-xs font-semibold tracking-widest text-amber-700 uppercase">Development only · P3-01</p>
	<h1 class="mt-1 text-2xl font-bold text-slate-950">Camera lab: capability probe</h1>
	<p class="mt-2 max-w-3xl text-sm text-slate-600">
		Finds out what the MacBook built-in camera actually delivers in this browser: resolutions, frame rate, controls, and still
		quality. Nothing is uploaded or saved, and the camera turns off when the test finishes. Turn off Video Effects (Center Stage,
		Portrait, Studio Light) first.
	</p>

	<div class="mt-6 flex flex-wrap gap-3">
		<button
			type="button"
			class="rounded-lg bg-indigo-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-indigo-500 disabled:opacity-50"
			disabled={running}
			onclick={run}>{running ? 'Testing… (about 15 s)' : 'Run camera test'}</button
		>
		{#if cameraOn}
			<button type="button" class="rounded-lg border border-red-300 px-4 py-2.5 text-sm font-semibold text-red-700" onclick={stopCamera}>
				Stop camera
			</button>
		{/if}
		{#if report}
			<button type="button" class="rounded-lg border border-slate-300 px-4 py-2.5 text-sm font-semibold text-slate-800 hover:bg-slate-50" onclick={download}>
				Download report (.json)
			</button>
			<button type="button" class="rounded-lg border border-slate-300 px-4 py-2.5 text-sm font-semibold text-slate-800 hover:bg-slate-50" onclick={copyReport}>
				{copyState === 'copied' ? 'Copied ✓ — paste it to Claude' : copyState === 'failed' ? 'Copy failed — use the text box below' : 'Copy report'}
			</button>
		{/if}
	</div>

	{#if errorText}
		<p class="mt-4 rounded-lg bg-red-50 px-4 py-3 text-sm text-red-800" role="alert">{errorText}</p>
	{/if}

	<div class="mt-6 grid gap-6 lg:grid-cols-2">
		<div>
			<div class="relative aspect-video overflow-hidden rounded-xl bg-slate-900">
				<!-- Mirrored for the user; measured frames are unmirrored. -->
				<video bind:this={video} class="size-full -scale-x-100 object-contain" muted playsinline></video>
				{#if !cameraOn}
					<p class="absolute inset-0 grid place-items-center text-sm text-slate-400">
						{previewUrl ? 'Camera off' : 'Camera off. Press "Run camera test".'}
					</p>
				{/if}
			</div>
			{#if previewUrl}
				<p class="mt-3 text-xs text-slate-500">Last still (kept only in this page, not saved):</p>
				<img src={previewUrl} alt="Last captured still" class="mt-1 w-full rounded-lg border border-slate-200" />
			{/if}
		</div>

		<pre class="max-h-112 overflow-auto rounded-xl bg-slate-950 p-4 text-xs leading-relaxed text-slate-200">{log.join('\n') || 'Log appears here.'}</pre>
	</div>

	{#if report}
		<section class="mt-8 space-y-6 text-sm">
			<div class="rounded-xl border p-4 {report.f1Pass ? 'border-emerald-300 bg-emerald-50' : 'border-amber-300 bg-amber-50'}">
				<strong>F1 (≥ 1280×720 delivered):</strong>
				{report.f1Pass === null ? 'unknown' : report.f1Pass ? 'PASS' : 'FAIL'} · {report.browser} · camera "{report.selectedCamera}" · measured
				{report.measuredFps ?? '—'} fps
			</div>

			<div>
				<h2 class="font-semibold text-slate-900">Resolution ladder</h2>
				<table class="mt-2 w-full text-left">
					<thead class="text-slate-500"><tr><th class="py-1">Requested</th><th>Delivered</th><th>fps</th><th>Error</th></tr></thead>
					<tbody>
						{#each report.ladder as row (row.requested)}
							<tr class="border-t border-slate-200">
								<td class="py-1">{row.requested}</td>
								<td>{row.width ? `${row.width}×${row.height}` : '—'}</td>
								<td>{row.frameRate ?? '—'}</td>
								<td class="text-red-700">{row.error ?? ''}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>

			<div>
				<h2 class="font-semibold text-slate-900">Still capture</h2>
				<table class="mt-2 w-full text-left">
					<thead class="text-slate-500"><tr><th class="py-1">Method</th><th>Size</th><th>Sharpness</th><th>JPEG size</th><th>Error</th></tr></thead>
					<tbody>
						{#each report.stills as s (s.method)}
							<tr class="border-t border-slate-200">
								<td class="py-1">{s.method}</td>
								<td>{s.width ? `${s.width}×${s.height}` : '—'}</td>
								<td>{s.sharpness ?? '—'}</td>
								<td>{s.jpegBytes ? `${Math.round(s.jpegBytes / 1024)} KB` : '—'}</td>
								<td class="text-red-700">{s.error ?? ''}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>

			<div>
				<h2 class="font-semibold text-slate-900">Controls the browser exposes (getCapabilities)</h2>
				<table class="mt-2 w-full text-left">
					<thead class="text-slate-500"><tr><th class="py-1">Control</th><th>Capability</th><th>Current setting</th></tr></thead>
					<tbody>
						{#each capabilityKeys as key (key)}
							<tr class="border-t border-slate-200">
								<td class="py-1 font-mono text-xs">{key}</td>
								<td class="font-mono text-xs">{show(report.capabilities?.[key])}</td>
								<td class="font-mono text-xs">{show(report.settings[key])}</td>
							</tr>
						{/each}
					</tbody>
				</table>
				<p class="mt-2 text-xs text-slate-500">Supported constraints: {report.supportedConstraints.join(', ')}</p>
			</div>

			<div>
				<h2 class="font-semibold text-slate-900">Raw report (select all and copy if the buttons don't work)</h2>
				<textarea
					readonly
					class="mt-2 h-48 w-full rounded-lg border border-slate-300 p-3 font-mono text-xs"
					value={JSON.stringify(report, null, 2)}
					onfocus={(e) => e.currentTarget.select()}
				></textarea>
			</div>
		</section>
	{/if}
</main>
