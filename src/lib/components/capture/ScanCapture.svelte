<script lang="ts" module>
	import type { ScanView } from '#lib/camera/scan-steps.ts';

	export interface Capture {
		view: ScanView;
		blob: Blob;
		url: string;
		width: number;
		height: number;
	}
</script>

<script lang="ts">
	import { onDestroy } from 'svelte';
	import { openCamera, stopStream } from '#lib/camera/media.ts';
	import {
		bodyYaw,
		eyeDistancePx,
		framing,
		type Landmark,
		LM,
		nearestBodyView,
		StillnessTracker
	} from '#lib/camera/pose-checks.ts';
	import { createPoseDetector, type PoseDetector } from '#lib/camera/pose-detector.ts';
	import { AutoCapture, FRAMING_TEXT, SCAN_STEPS, type ScanStep } from '#lib/camera/scan-steps.ts';

	interface Props {
		/** Called with all captures when the user clicks "Save scan" (Milestone 1, M1-05). */
		onsave: (captures: Capture[]) => Promise<void>;
	}
	let { onsave }: Props = $props();

	type Stage = 'idle' | 'starting' | 'calibrate' | 'capture' | 'review' | 'saving';

	let stage = $state<Stage>('idle');
	let stepIndex = $state(0);
	let returnToReview = $state(false); // retaking a single view from the review screen
	let captures = $state<Record<string, Capture>>({});
	let errorText = $state<string | null>(null);

	// Live analysis shown to the user
	let hint = $state('');
	let people = $state(0);
	let inFrame = $state(false);
	let still = $state(false);
	let facing = $state<string | null>(null);
	let countdown = $state(0);
	let flash = $state(false);

	let video: HTMLVideoElement | undefined = $state();
	let overlay: HTMLCanvasElement | undefined = $state();
	let stream: MediaStream | null = null;
	let detector: PoseDetector | null = null;
	let raf = 0;
	let lastDetect = 0;
	const tracker = new StillnessTracker(1000, 0.012);
	const auto = new AutoCapture(3000);

	const step = $derived<ScanStep>(SCAN_STEPS[stepIndex]);
	const capturedCount = $derived(Object.keys(captures).length);

	// ---- camera lifecycle ---------------------------------------------------------------

	async function startCamera() {
		errorText = null;
		stage = 'starting';
		try {
			detector ??= await createPoseDetector();
			stream = await openCamera({ width: 1920, height: 1080 });
			video!.srcObject = stream;
			await video!.play();
			tracker.reset();
			auto.reset(true);
			raf = requestAnimationFrame(loop);
			stage = returnToReview ? 'capture' : 'calibrate';
		} catch (e) {
			stopCamera();
			stage = 'idle';
			errorText =
				e instanceof DOMException && e.name === 'NotAllowedError'
					? 'Camera access was blocked. Allow it in the address bar and in System Settings → Privacy & Security → Camera, then try again.'
					: e instanceof DOMException && e.name === 'NotReadableError'
						? 'The camera is in use by another app (FaceTime, Zoom, Photo Booth…). Close it and try again.'
						: e instanceof Error
							? e.message
							: String(e);
		}
	}

	function stopCamera() {
		// onDestroy also runs during server rendering, where browser APIs don't exist.
		if (raf) cancelAnimationFrame(raf);
		raf = 0;
		stopStream(stream);
		stream = null;
		if (video) video.srcObject = null;
	}

	onDestroy(() => {
		stopCamera();
		detector?.close();
		Object.values(captures).forEach((c) => URL.revokeObjectURL(c.url));
	});

	$effect(() => {
		const off = () => stopCamera();
		window.addEventListener('pagehide', off);
		return () => window.removeEventListener('pagehide', off);
	});

	// ---- per-frame analysis ---------------------------------------------------------------

	function loop(now: number) {
		raf = requestAnimationFrame(loop);
		if (!video || !detector || video.readyState < 2 || now - lastDetect < 66) return; // ~15 fps
		lastDetect = now;

		const result = detector.detect(video, now);
		people = result.people.length;
		const person = result.people[0];
		let ready = false;
		let moving = true;

		if (people === 0) {
			hint = 'Step into view';
			inFrame = still = false;
			tracker.reset();
		} else if (people > 1) {
			hint = 'Only the person being scanned should be in view';
			inFrame = still = false;
		} else {
			still = tracker.push(now, person.landmarks);
			moving = !still;
			if (stage === 'calibrate' || step.kind === 'body') {
				const f = framing(person.landmarks);
				inFrame = f.fullBodyVisible;
				facing = person.world.length ? nearestBodyView(bodyYaw(person.world)) : null;
				hint = inFrame ? (still ? 'Hold still…' : 'Good. Now hold still') : FRAMING_TEXT[f.hint];
				ready = inFrame && still;
			} else {
				facing = null;
				const eyes = eyeDistancePx(person.landmarks, video.videoWidth, video.videoHeight);
				inFrame = (person.landmarks[LM.nose].visibility ?? 1) > 0.5;
				hint =
					step.view === 'face_front' && eyes < 100
						? 'Come a little closer to the camera'
						: still
							? 'Hold still…'
							: 'Now hold still';
				ready = inFrame && still;
			}
		}
		draw(person?.landmarks, ready);

		if (stage === 'calibrate') {
			if (ready) {
				stage = 'capture';
				auto.reset(true);
				tracker.reset();
			}
			return;
		}
		if (stage !== 'capture') return;

		const state = auto.update(now, { ready, moving });
		countdown = state.phase === 'countdown' ? state.remaining : 0;
		if (state.phase === 'capture') takePhoto();
	}

	function draw(lm: Landmark[] | undefined, ready: boolean) {
		if (!overlay || !video) return;
		overlay.width = video.videoWidth;
		overlay.height = video.videoHeight;
		const ctx = overlay.getContext('2d')!;
		ctx.clearRect(0, 0, overlay.width, overlay.height);
		if (!lm) return;
		ctx.fillStyle = ready ? '#22c55e' : '#f59e0b';
		for (const p of lm) {
			if ((p.visibility ?? 1) < 0.3) continue;
			ctx.beginPath();
			ctx.arc(p.x * overlay.width, p.y * overlay.height, Math.max(4, overlay.width / 300), 0, Math.PI * 2);
			ctx.fill();
		}
	}

	// ---- capture ------------------------------------------------------------------------------

	function beep() {
		try {
			const audio = new AudioContext();
			const osc = audio.createOscillator();
			osc.frequency.value = 880;
			osc.connect(audio.destination);
			osc.start();
			osc.stop(audio.currentTime + 0.12);
			osc.onended = () => audio.close();
		} catch {
			// Sound is optional.
		}
	}

	function takePhoto() {
		if (!video) return;
		const view = step.view;
		const canvas = document.createElement('canvas');
		canvas.width = video.videoWidth;
		canvas.height = video.videoHeight;
		canvas.getContext('2d')!.drawImage(video, 0, 0); // unmirrored
		beep();
		flash = true;
		setTimeout(() => (flash = false), 150);
		canvas.toBlob(
			(blob) => {
				if (!blob) return;
				const old = captures[view];
				if (old) URL.revokeObjectURL(old.url);
				captures[view] = { view, blob, url: URL.createObjectURL(blob), width: canvas.width, height: canvas.height };
			},
			'image/jpeg',
			0.92
		);
		advance();
	}

	function advance() {
		countdown = 0;
		tracker.reset();
		if (returnToReview || stepIndex === SCAN_STEPS.length - 1) {
			returnToReview = false;
			finishCapture();
			return;
		}
		stepIndex += 1;
		auto.reset(false); // wait until the person has turned
	}

	function finishCapture() {
		stopCamera(); // camera is not needed for the review
		stage = 'review';
	}

	function captureNow() {
		if (stage === 'capture') auto.trigger(performance.now());
	}

	function goBack() {
		if (stepIndex > 0) {
			stepIndex -= 1;
			auto.reset(true);
			tracker.reset();
		}
	}

	function retake(index: number) {
		stepIndex = index;
		returnToReview = true;
		startCamera();
	}

	function startOver() {
		Object.values(captures).forEach((c) => URL.revokeObjectURL(c.url));
		captures = {};
		stepIndex = 0;
		returnToReview = false;
		startCamera();
	}

	async function save() {
		stage = 'saving';
		errorText = null;
		try {
			await onsave(SCAN_STEPS.map((s) => captures[s.view]).filter(Boolean));
		} catch (e) {
			errorText = e instanceof Error ? e.message : 'Saving failed. Please try again.';
			stage = 'review';
		}
	}

	function onkeydown(e: KeyboardEvent) {
		if (e.code === 'Space' && stage === 'capture') {
			e.preventDefault();
			captureNow();
		}
	}

	const live = $derived(stage === 'starting' || stage === 'calibrate' || stage === 'capture');
	const missingRequired = $derived(
		SCAN_STEPS.filter((s) => s.kind === 'body' && !captures[s.view]).length +
			Math.max(0, 3 - SCAN_STEPS.filter((s) => s.kind === 'face' && captures[s.view]).length)
	);
</script>

<svelte:window {onkeydown} />

{#if errorText}
	<p class="mb-4 rounded-lg bg-red-50 px-4 py-3 text-sm text-red-800" role="alert">{errorText}</p>
{/if}

{#if stage === 'idle'}
	<button
		type="button"
		class="rounded-lg bg-indigo-600 px-6 py-3 text-base font-semibold text-white hover:bg-indigo-500"
		onclick={startCamera}>Start camera</button
	>
{/if}

<!-- Live camera: kept in the DOM while capturing so the <video> element persists -->
<div class:hidden={!live}>
	<div class="flex flex-wrap items-baseline justify-between gap-2">
		<p class="text-sm font-semibold tracking-wide text-indigo-700 uppercase">
			{#if stage === 'calibrate' || stage === 'starting'}
				Step 1 · Stand on your mark
			{:else}
				{step.kind === 'body' ? 'Body' : 'Face'} · {SCAN_STEPS.indexOf(step) + 1} of {SCAN_STEPS.length} · {step.label}
			{/if}
		</p>
		<div class="flex gap-1.5" aria-label="Progress">
			{#each SCAN_STEPS as s (s.view)}
				<span class="size-2.5 rounded-full {captures[s.view] ? 'bg-emerald-500' : s === step && stage === 'capture' ? 'bg-indigo-600' : 'bg-slate-300'}"></span>
			{/each}
		</div>
	</div>

	<h2 class="mt-2 text-4xl leading-tight font-bold text-slate-950 sm:text-5xl" aria-live="polite">
		{#if stage === 'starting'}
			Starting camera…
		{:else if stage === 'calibrate'}
			Stand on your mark, about 2.5 m away
		{:else}
			{step.instruction}
		{/if}
	</h2>

	<div class="relative mt-4 aspect-video overflow-hidden rounded-2xl bg-slate-900">
		<video bind:this={video} class="absolute inset-0 size-full -scale-x-100 object-contain" muted playsinline></video>
		<canvas bind:this={overlay} class="pointer-events-none absolute inset-0 size-full -scale-x-100 object-contain"></canvas>
		{#if countdown > 0}
			<div class="absolute inset-0 grid place-items-center">
				<span class="text-[12rem] leading-none font-black text-white drop-shadow-[0_4px_16px_rgba(0,0,0,0.6)]">{countdown}</span>
			</div>
		{/if}
		{#if flash}<div class="absolute inset-0 bg-white/70"></div>{/if}
		<p class="absolute inset-x-0 bottom-0 bg-slate-950/70 px-4 py-3 text-center text-2xl font-semibold text-white">
			{hint || '…'}
		</p>
	</div>

	<div class="mt-3 flex flex-wrap items-center gap-2 text-sm">
		<span class="rounded-full px-3 py-1 {people === 1 ? 'bg-emerald-50 text-emerald-800' : 'bg-amber-50 text-amber-800'}">
			{people === 1 ? 'One person ✓' : people === 0 ? 'No person' : 'More than one person'}
		</span>
		<span class="rounded-full px-3 py-1 {inFrame ? 'bg-emerald-50 text-emerald-800' : 'bg-amber-50 text-amber-800'}">
			{step.kind === 'face' && stage === 'capture' ? 'Face visible' : 'Whole body visible'}
			{inFrame ? '✓' : '✗'}
		</span>
		<span class="rounded-full px-3 py-1 {still ? 'bg-emerald-50 text-emerald-800' : 'bg-slate-100 text-slate-600'}">
			{still ? 'Still ✓' : 'Moving'}
		</span>
		{#if facing && stage === 'capture' && step.kind === 'body'}
			<span class="rounded-full bg-slate-100 px-3 py-1 text-slate-700" title="Estimated from your pose (hint only)">
				Looks like: {SCAN_STEPS.find((s) => s.view === facing)?.label}
			</span>
		{/if}
		<span class="ml-auto flex gap-2">
			{#if stage === 'capture' && stepIndex > 0 && !returnToReview}
				<button type="button" class="rounded-lg border border-slate-300 px-3 py-1.5 font-medium text-slate-700 hover:bg-slate-50" onclick={goBack}>
					← Previous
				</button>
			{/if}
			{#if stage === 'calibrate'}
				<button
					type="button"
					class="rounded-lg border border-slate-300 px-3 py-1.5 font-medium text-slate-700 hover:bg-slate-50"
					title="Use this if the check never turns green. You can still capture with Space."
					onclick={() => {
						stage = 'capture';
						auto.reset(true);
					}}>Skip this check</button
				>
			{/if}
			{#if stage === 'capture'}
				<button type="button" class="rounded-lg bg-slate-900 px-3 py-1.5 font-medium text-white hover:bg-slate-700" onclick={captureNow}>
					Capture now (Space)
				</button>
			{/if}
			<button type="button" class="rounded-lg border border-red-300 px-3 py-1.5 font-medium text-red-700 hover:bg-red-50" onclick={finishCapture}>
				Stop camera
			</button>
		</span>
	</div>
	<p class="mt-2 text-xs text-slate-500">
		Photos are taken automatically when you are in view and still (3-2-1). Nothing leaves this browser until you click Save.
	</p>
</div>

{#if stage === 'review' || stage === 'saving'}
	<h2 class="text-3xl font-bold text-slate-950">Check your photos</h2>
	<p class="mt-1 text-sm text-slate-600">
		{capturedCount} of {SCAN_STEPS.length} taken. Click a photo to retake it. You need all 8 body views and at least 3 face photos.
	</p>
	<div class="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4 lg:grid-cols-5">
		{#each SCAN_STEPS as s, i (s.view)}
			<button
				type="button"
				class="group overflow-hidden rounded-xl border text-left {captures[s.view] ? 'border-slate-200' : 'border-dashed border-amber-400'}"
				disabled={stage === 'saving'}
				onclick={() => retake(i)}
			>
				<div class="aspect-video bg-slate-100">
					{#if captures[s.view]}
						<img src={captures[s.view].url} alt={s.label} class="size-full object-cover" />
					{:else}
						<div class="grid size-full place-items-center text-xs text-amber-700">Missing: take photo</div>
					{/if}
				</div>
				<p class="flex justify-between px-2 py-1.5 text-xs">
					<span class="font-medium text-slate-800">{s.label}</span>
					<span class="text-indigo-600 group-hover:underline">{captures[s.view] ? 'Retake' : 'Take'}</span>
				</p>
			</button>
		{/each}
	</div>
	<div class="mt-6 flex flex-wrap items-center gap-3">
		<button
			type="button"
			class="rounded-lg bg-indigo-600 px-6 py-3 text-base font-semibold text-white hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
			disabled={missingRequired > 0 || stage === 'saving'}
			onclick={save}>{stage === 'saving' ? 'Saving…' : 'Save scan'}</button
		>
		<button type="button" class="rounded-lg border border-slate-300 px-4 py-3 text-sm font-semibold text-slate-700 hover:bg-slate-50" disabled={stage === 'saving'} onclick={startOver}>
			Start over
		</button>
		{#if missingRequired > 0}
			<span class="text-sm text-amber-700">{missingRequired} more photo{missingRequired === 1 ? '' : 's'} needed</span>
		{/if}
	</div>
{/if}
