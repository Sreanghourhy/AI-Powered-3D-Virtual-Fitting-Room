<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/state';
	import { DISCLAIMERS } from '#lib/components/consent/disclaimers.ts';
	import ModelViewer from '#lib/components/fitting-room/ModelViewer.svelte';
	import GarmentPicker from '#lib/components/garments/GarmentPicker.svelte';
	import { outfitFromParams, outfitQuery } from '#lib/components/garments/outfit.ts';
	import type { Outfit } from '#lib/types/garment.ts';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();

	const shirts = $derived(data.garments.filter((g) => g.category === 'top'));
	const pants = $derived(data.garments.filter((g) => g.category === 'bottom'));
	const outfit = $derived(outfitFromParams(page.url.searchParams, data.garments));

	// Changing one slot keeps the other (FR-04: shirts and pants are independent).
	function select(change: Partial<Outfit>) {
		goto(`${page.url.pathname}${outfitQuery({ ...outfit, ...change })}`, {
			replaceState: true,
			reset: false // keep scroll position and focus
		});
	}
</script>

<svelte:head><title>Try-On · Fitting Room</title></svelte:head>

<main class="mx-auto grid max-w-6xl gap-6 px-4 py-6 sm:px-6 lg:grid-cols-[1fr_20rem] lg:py-10">
	<section class="relative h-[60vh] min-h-80 overflow-hidden rounded-2xl border border-slate-200 bg-gradient-to-b from-slate-50 to-slate-200 lg:h-[75vh]">
		<p class="absolute inset-x-3 top-3 z-10 rounded-lg bg-white/90 px-3 py-2 text-xs font-medium text-slate-700 shadow-sm">
			ⓘ {DISCLAIMERS.tryOn}
		</p>
		<ModelViewer url="/models/sample.glb" />
		<p class="absolute inset-x-3 bottom-3 z-10 rounded-lg bg-amber-50/95 px-3 py-2 text-xs text-amber-900 shadow-sm">
			Sample model, not you. Your own scanned model appears here once you're scanned.
		</p>
	</section>

	<aside class="space-y-6">
		<GarmentPicker label="Shirt" garments={shirts} selectedId={outfit.topId} onselect={(id) => select({ topId: id })} />
		<GarmentPicker label="Pants" garments={pants} selectedId={outfit.bottomId} onselect={(id) => select({ bottomId: id })} />
		<p class="rounded-xl border border-dashed border-slate-300 bg-slate-50 p-3 text-xs text-slate-600">
			Garments are shown on the 3D model from Phase 6. For now, your selection is kept in the page link.
		</p>
	</aside>
</main>
