<script lang="ts">
	import { goto, invalidateAll } from '$app/navigation';
	import { saveScan as uploadScan } from '#lib/camera/save-scan.ts';
	import ScanCapture, { type Capture } from '#lib/components/capture/ScanCapture.svelte';
	import Modal from '#lib/components/ui/Modal.svelte';
	import PrivacyNoticeText from '#lib/components/ui/PrivacyNoticeText.svelte';
	import { getFlag, PRIVACY_NOTICE_SEEN, setFlag } from '#lib/utils/local-flag.ts';

	// Shown before the camera is used, unless dismissed with "Don't show again" (FR-12).
	let noticeOpen = $state(false);
	let dontShowAgain = $state(false);

	$effect(() => {
		noticeOpen = !getFlag(PRIVACY_NOTICE_SEEN);
	});

	async function saveScan(captures: Capture[], onprogress: (done: number, total: number) => void) {
		await uploadScan(
			captures.map((c) => ({ view: c.view, blob: c.blob })),
			onprogress
		);
		await invalidateAll();
		await goto('/');
	}

	function acceptNotice() {
		if (dontShowAgain) setFlag(PRIVACY_NOTICE_SEEN, true);
		noticeOpen = false;
	}
</script>

<svelte:head><title>Scan · Fitting Room</title></svelte:head>

<Modal open={noticeOpen} title="Before you scan" onclose={() => noticeOpen && goto('/')}>
	<PrivacyNoticeText />
	<label class="mt-4 flex items-center gap-2 text-slate-700">
		<input type="checkbox" bind:checked={dontShowAgain} class="size-4 accent-indigo-600" />
		Don't show this again
	</label>
	{#snippet actions()}
		<a href="/" class="rounded-lg border border-slate-300 px-4 py-2 font-semibold text-slate-700 hover:bg-slate-50">Cancel</a>
		<button type="button" class="rounded-lg bg-indigo-600 px-4 py-2 font-semibold text-white hover:bg-indigo-500" onclick={acceptNotice}>
			Continue
		</button>
	{/snippet}
</Modal>

<main class="mx-auto max-w-6xl px-4 py-6 sm:px-6">
	<a href="/" class="text-sm font-medium text-indigo-600 hover:underline">← Back to fitting room</a>
	<h1 class="mt-3 text-2xl font-bold text-slate-950">Scan</h1>

	<details class="mt-3 rounded-xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-700" open>
		<summary class="cursor-pointer font-semibold text-slate-900">Before you start (1 minute)</summary>
		<ul class="mt-3 grid gap-2 sm:grid-cols-2">
			<li>☐ Laptop on a table, screen facing where you will stand</li>
			<li>☐ Bright, even light in front of you. No window behind you.</li>
			<li>☐ Fitted, plain clothes. Hair tied back. No glasses or hat.</li>
			<li>☐ <strong>Video effects off:</strong> Control Center → Video Effects → Center Stage, Portrait, Studio Light</li>
			<li>☐ A spot (X) on the floor about 2.5 m from the laptop</li>
			<li>☐ Turn the sound on: you'll hear a beep for each photo</li>
		</ul>
		<button type="button" class="mt-3 text-xs text-slate-500 underline" onclick={() => (noticeOpen = true)}>Show privacy notice</button>
	</details>

	<div class="mt-6">
		<ScanCapture onsave={saveScan} />
	</div>
</main>
