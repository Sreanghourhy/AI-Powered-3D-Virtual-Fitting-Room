<script lang="ts">
	import type { Garment } from '#lib/types/garment.ts';

	let { garment }: { garment: Garment } = $props();

	const tryOnHref = $derived(`/try-on?${garment.category}=${encodeURIComponent(garment.id)}`);
</script>

<article class="group flex flex-col overflow-hidden rounded-2xl border border-slate-200 bg-white">
	<div class="aspect-square bg-slate-100">
		<img
			src={garment.thumbnailUrl}
			alt={garment.name}
			width="512"
			height="512"
			loading="lazy"
			class="size-full object-contain transition group-hover:scale-[1.02]"
		/>
	</div>
	<div class="flex flex-1 flex-col gap-2 p-4">
		<h2 class="text-sm font-semibold text-slate-900">{garment.name}</h2>
		{#if garment.sizes?.length}
			<p class="text-xs text-slate-500">Sizes {garment.sizes.join(' · ')}</p>
		{/if}
		<a
			href={tryOnHref}
			class="mt-auto inline-flex items-center justify-center rounded-lg bg-indigo-600 px-3 py-2 text-sm font-semibold text-white hover:bg-indigo-500"
			>Try on →</a
		>
	</div>
</article>
