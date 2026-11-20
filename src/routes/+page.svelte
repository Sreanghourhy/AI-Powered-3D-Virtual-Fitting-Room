<script lang="ts">
	import { goto, invalidateAll } from '$app/navigation';
	import { page } from '$app/state';
	import FittingRoomStage from '#lib/components/fitting-room/FittingRoomStage.svelte';
	import type { ModelState } from '#lib/components/fitting-room/model-state.ts';
	import GarmentPicker from '#lib/components/garments/GarmentPicker.svelte';
	import { outfitFromParams, outfitQuery } from '#lib/components/garments/outfit.ts';
	import { ApiError, discardAll } from '#lib/api/client.ts';
	import BackendOfflineNotice from '#lib/components/ui/BackendOfflineNotice.svelte';
	import BackendStatus from '#lib/components/ui/BackendStatus.svelte';
	import Modal from '#lib/components/ui/Modal.svelte';
	import type { Outfit } from '#lib/types/garment.ts';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();

	// Until a real model exists the stage shows no body: no sample or generic avatar
	// is ever shown in its place (FR-07). Milestone 2 adds generating/ready/failed.
	const modelState = $derived<ModelState>(
		data.scan
			? { kind: 'scanned', photos: data.scan.images.length, savedAt: data.scan.completedAt ?? data.scan.createdAt }
			: { kind: 'none' }
	);

	const shirts = $derived(data.garments.filter((g) => g.category === 'top'));
	const pants = $derived(data.garments.filter((g) => g.category === 'bottom'));
	const outfit = $derived(outfitFromParams(page.url.searchParams, data.garments));

	let discardOpen = $state(false);
	let discarding = $state(false);
	let discardMessage = $state<{ ok: boolean; text: string } | null>(null);

	async function discard() {
		discarding = true;
		try {
			await discardAll();
			discardMessage = { ok: true, text: 'Your scan photos, 3D model and outfit were deleted from this MacBook.' };
			discardOpen = false;
			await goto('/', { replaceState: true });
			await invalidateAll();
		} catch (e) {
			discardMessage = { ok: false, text: e instanceof ApiError ? e.message : 'Discard failed. Please try again.' };
			discardOpen = false;
		} finally {
			discarding = false;
		}
	}

	// Changing one slot keeps the other: shirts and pants are independent (FR-09).
	function select(change: Partial<Outfit>) {
		goto(`/${outfitQuery({ ...outfit, ...change })}`, { replaceState: true, reset: false });
	}
</script>

<svelte:head>
	<title>Fitting Room</title>
	<meta name="description" content="Scan yourself with your MacBook camera and try on shirts and pants on your own 3D model." />
</svelte:head>

<main class="mx-auto grid max-w-7xl gap-6 px-4 py-6 sm:px-6 lg:grid-cols-[1fr_20rem]">
	<FittingRoomStage state={modelState} />

	<aside class="flex flex-col gap-6">
		{#if data.backendError}
			<BackendOfflineNotice message={data.backendError} />
		{/if}
		<GarmentPicker label="Shirt" garments={shirts} selectedId={outfit.topId} onselect={(id) => select({ topId: id })} />
		<GarmentPicker label="Pants" garments={pants} selectedId={outfit.bottomId} onselect={(id) => select({ bottomId: id })} />
		{#if modelState.kind !== 'ready'}
			<p class="rounded-xl border border-dashed border-slate-300 bg-slate-50 p-3 text-xs text-slate-600">
				You can pick clothes now. They appear on your 3D model once it has been generated.
			</p>
		{/if}

		<div class="mt-auto flex flex-col gap-3 border-t border-slate-200 pt-4 text-sm">
			<a href="/scan" class="font-medium text-indigo-600 hover:underline">{modelState.kind === 'none' ? 'Start Scan' : 'Rescan'}</a>
			<button type="button" class="self-start font-medium text-red-600 hover:underline" onclick={() => (discardOpen = true)}>
				Discard scan & model
			</button>
			{#if discardMessage}
				<p class="rounded-lg px-3 py-2 text-xs {discardMessage.ok ? 'bg-emerald-50 text-emerald-800' : 'bg-red-50 text-red-700'}" role="status">
					{discardMessage.text}
				</p>
			{/if}
			<div><BackendStatus /></div>
		</div>
	</aside>
</main>

<Modal open={discardOpen} title="Discard scan & model?" onclose={() => (discardOpen = false)}>
	<p>This deletes your scan photos, your 3D model and your outfit from this MacBook. It can't be undone.</p>
	{#snippet actions()}
		<button type="button" class="rounded-lg border border-slate-300 px-4 py-2 font-semibold text-slate-700 hover:bg-slate-50" onclick={() => (discardOpen = false)}>
			Cancel
		</button>
		<button
			type="button"
			class="rounded-lg bg-red-600 px-4 py-2 font-semibold text-white hover:bg-red-500 disabled:opacity-50"
			disabled={discarding}
			onclick={discard}>{discarding ? 'Deleting…' : 'Delete everything'}</button
		>
	{/snippet}
</Modal>
