<script lang="ts">
	import { goto, invalidateAll } from '$app/navigation';
	import { acceptConsent, ApiError, withdrawConsent } from '#lib/api/client.ts';
	import ConsentText from '#lib/components/consent/ConsentText.svelte';
	import { DISCLAIMERS } from '#lib/components/consent/disclaimers.ts';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();

	let confirmsAdult = $state(false);
	let agrees = $state(false);
	let busy = $state(false);
	let error = $state<string | null>(null);
	let confirmWithdraw = $state(false);

	const status = $derived(data.consent);
	const active = $derived(
		status.consents.find((c) => c.version === status.requiredVersion && c.withdrawnAt === null)
	);
	const hadOlderVersion = $derived(
		!status.accepted && status.consents.some((c) => c.version !== status.requiredVersion && !c.withdrawnAt)
	);

	const formatDate = (iso: string) =>
		new Date(iso).toLocaleDateString(undefined, { day: 'numeric', month: 'short', year: 'numeric' });

	async function run(action: () => Promise<unknown>, next?: string) {
		busy = true;
		error = null;
		try {
			await action();
			await invalidateAll();
			if (next) await goto(next);
		} catch (e) {
			error = e instanceof ApiError ? e.message : 'Something went wrong. Please try again.';
		} finally {
			busy = false;
		}
	}
</script>

<svelte:head><title>Consent · Fitting Room</title></svelte:head>

<main class="mx-auto max-w-2xl px-4 py-10 sm:px-6">
	{#if status.accepted && active}
		<h1 class="text-2xl font-bold text-slate-950">Privacy & consent</h1>
		<div class="mt-6 rounded-xl border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-900">
			You agreed to consent <strong>{active.version}</strong> on {formatDate(active.grantedAt)}.
		</div>
		<a
			href="/capture"
			class="mt-6 inline-flex rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-indigo-500"
			>Continue to capture</a
		>

		<details class="mt-10 text-sm text-slate-600">
			<summary class="cursor-pointer font-medium text-slate-800">Read the consent text again</summary>
			<div class="mt-4"><ConsentText /></div>
		</details>

		<section class="mt-10 rounded-xl border border-slate-200 p-4">
			<h2 class="font-semibold text-slate-900">Withdraw consent</h2>
			<p class="mt-1 text-sm text-slate-600">
				If you withdraw, we delete your scan photos and 3D model, and you can't scan again until you agree again.
			</p>
			{#if confirmWithdraw}
				<div class="mt-4 flex flex-wrap gap-3">
					<button
						type="button"
						class="rounded-lg bg-red-600 px-4 py-2 text-sm font-semibold text-white hover:bg-red-500 disabled:opacity-50"
						disabled={busy}
						onclick={() => run(() => withdrawConsent(active.id))}>Yes, withdraw and delete my scan data</button
					>
					<button
						type="button"
						class="rounded-lg border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700"
						onclick={() => (confirmWithdraw = false)}>Cancel</button
					>
				</div>
			{:else}
				<button
					type="button"
					class="mt-4 text-sm font-medium text-red-600 hover:underline"
					onclick={() => (confirmWithdraw = true)}>Withdraw consent</button
				>
			{/if}
		</section>
	{:else}
		<h1 class="text-2xl font-bold text-slate-950">Before we scan you</h1>
		{#if hadOlderVersion}
			<p class="mt-4 rounded-lg bg-amber-50 px-3 py-2 text-sm text-amber-900">
				We updated our consent text. Please review it again.
			</p>
		{/if}

		<div class="mt-6"><ConsentText /></div>

		<p class="mt-6 rounded-lg border border-amber-200 bg-amber-50 px-4 py-3 text-sm font-medium text-amber-900">
			⚠ {DISCLAIMERS.tryOn}
		</p>

		<form
			class="mt-6 space-y-3"
			onsubmit={(e) => {
				e.preventDefault();
				run(() => acceptConsent(status.requiredVersion), '/capture');
			}}
		>
			<label class="flex items-start gap-3 text-sm text-slate-800">
				<input type="checkbox" bind:checked={confirmsAdult} class="mt-0.5 size-4 accent-indigo-600" />
				<span><strong>I am 18 or older and I am the person being scanned.</strong></span>
			</label>
			<label class="flex items-start gap-3 text-sm text-slate-800">
				<input type="checkbox" bind:checked={agrees} class="mt-0.5 size-4 accent-indigo-600" />
				<span><strong>I agree to the capture and storage of my photos and 3D model as described above.</strong></span>
			</label>

			<div class="flex flex-wrap gap-3 pt-3">
				<a href="/catalog" class="rounded-lg border border-slate-300 px-4 py-2.5 text-sm font-semibold text-slate-700 hover:bg-slate-50"
					>Decline</a
				>
				<button
					type="submit"
					disabled={!confirmsAdult || !agrees || busy}
					class="rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
					>{busy ? 'Saving…' : 'Agree and continue'}</button
				>
			</div>
			<p class="text-xs text-slate-500">Declining keeps your account. You can still browse the catalog and scan later.</p>
		</form>
	{/if}

	{#if error}
		<p class="mt-4 rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700" role="alert">{error}</p>
	{/if}
</main>
