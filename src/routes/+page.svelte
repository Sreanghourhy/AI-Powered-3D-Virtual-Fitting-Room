<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/state';
	import FittingRoomStage from '#lib/components/fitting-room/FittingRoomStage.svelte';
	import type { ModelState } from '#lib/components/fitting-room/model-state.ts';
	import GarmentPicker from '#lib/components/garments/GarmentPicker.svelte';
	import { outfitFromParams, outfitQuery } from '#lib/components/garments/outfit.ts';
	import BackendStatus from '#lib/components/ui/BackendStatus.svelte';
	import type { Outfit } from '#lib/types/garment.ts';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();

	// Scans and models arrive in Phases 3–5. Until a real model exists, the stage
	// stays empty: no sample or generic avatar is ever shown in its place (FR-07).
	const modelState = { kind: 'none' } as ModelState;

	const shirts = $derived(data.garments.filter((g) => g.category === 'top'));
	const pants = $derived(data.garments.filter((g) => g.category === 'bottom'));
	const outfit = $derived(outfitFromParams(page.url.searchParams, data.garments));

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
		<GarmentPicker label="Shirt" garments={shirts} selectedId={outfit.topId} onselect={(id) => select({ topId: id })} />
		<GarmentPicker label="Pants" garments={pants} selectedId={outfit.bottomId} onselect={(id) => select({ bottomId: id })} />
		{#if modelState.kind !== 'ready'}
			<p class="rounded-xl border border-dashed border-slate-300 bg-slate-50 p-3 text-xs text-slate-600">
				You can pick clothes now. They appear on your 3D model once it has been generated.
			</p>
		{/if}

		<div class="mt-auto flex flex-col gap-3 border-t border-slate-200 pt-4 text-sm">
			<a href="/scan" class="font-medium text-indigo-600 hover:underline">{modelState.kind === 'none' ? 'Start Scan' : 'Rescan'}</a>
			<div><BackendStatus /></div>
		</div>
	</aside>
</main>
