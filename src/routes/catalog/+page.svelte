<script lang="ts">
	import GarmentCard from '#lib/components/garments/GarmentCard.svelte';
	import BackendOfflineNotice from '#lib/components/ui/BackendOfflineNotice.svelte';
	import { CATEGORIES } from '#lib/components/garments/categories.ts';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();
</script>

<svelte:head><title>Catalog · Fitting Room</title></svelte:head>

<main class="mx-auto max-w-6xl px-4 py-10 sm:px-6">
	<div class="flex flex-wrap items-end justify-between gap-4">
		<h1 class="text-2xl font-bold text-slate-950">Catalog</h1>
		<div class="inline-flex rounded-lg border border-slate-200 bg-slate-50 p-1" role="tablist" aria-label="Category">
			{#each CATEGORIES as cat (cat.id)}
				<a
					href="?category={cat.id}"
					role="tab"
					aria-selected={data.category === cat.id}
					data-sveltekit-noscroll
					class="rounded-md px-4 py-1.5 text-sm font-medium {data.category === cat.id
						? 'bg-white text-slate-900 shadow-sm'
						: 'text-slate-600 hover:text-slate-900'}">{cat.label}</a
				>
			{/each}
		</div>
	</div>

	{#if data.backendError}
		<div class="mt-8"><BackendOfflineNotice message={data.backendError} /></div>
	{:else if data.garments.length === 0}
		<p class="mt-10 rounded-xl border border-dashed border-slate-300 p-8 text-center text-slate-600">
			No items in this category yet.
		</p>
	{:else}
		<div class="mt-8 grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
			{#each data.garments as garment (garment.id)}
				<GarmentCard {garment} />
			{/each}
		</div>
	{/if}
</main>
