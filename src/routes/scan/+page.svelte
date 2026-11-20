<script lang="ts">
	import { goto } from '$app/navigation';
	import Modal from '#lib/components/ui/Modal.svelte';
	import PrivacyNoticeText from '#lib/components/ui/PrivacyNoticeText.svelte';
	import { getFlag, PRIVACY_NOTICE_SEEN, setFlag } from '#lib/utils/local-flag.ts';

	// Shown before the camera is used, unless dismissed with "Don't show again" (FR-12).
	let noticeOpen = $state(false);
	let dontShowAgain = $state(false);

	$effect(() => {
		noticeOpen = !getFlag(PRIVACY_NOTICE_SEEN);
	});

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

<main class="mx-auto max-w-2xl px-4 py-10 sm:px-6">
	<a href="/" class="text-sm font-medium text-indigo-600 hover:underline">← Back to fitting room</a>
	<h1 class="mt-4 text-2xl font-bold text-slate-950">Get ready (1 minute)</h1>
	<ul class="mt-6 space-y-3 text-slate-700">
		<li>☐ Laptop on a table, nothing moving behind you</li>
		<li>☐ Bright, even light in front of you. No window behind you.</li>
		<li>☐ Fitted, plain clothes. Hair tied back. No glasses or hat.</li>
		<li>☐ Video effects off: Control Center → Video Effects → Center Stage, Portrait, Studio Light off</li>
		<li>☐ A marked spot (X) on the floor about 2.5 m from the laptop</li>
	</ul>
	<p class="mt-8 rounded-xl border border-dashed border-slate-300 bg-slate-50 p-4 text-sm text-slate-600">
		The guided MacBook camera capture is being built in Phase 3. The camera is not used yet.
	</p>
	<button type="button" class="mt-4 text-sm text-slate-500 underline" onclick={() => (noticeOpen = true)}>Show privacy notice</button>
</main>
