<script lang="ts">
	import { DISCLAIMERS } from '#lib/components/consent/disclaimers.ts';
</script>

<svelte:head><title>My 3D model · Fitting Room</title></svelte:head>

<!-- Phase 2: empty state only. Processing / ready / failed states come in Phase 5 (docs/wireframes/my-model.md). -->
<main class="mx-auto max-w-2xl px-4 py-10 sm:px-6">
	<h1 class="text-2xl font-bold text-slate-950">My 3D model</h1>

	<section class="mt-6 rounded-2xl border border-slate-200 p-6 text-center sm:p-10">
		<div class="mx-auto grid size-28 place-items-center rounded-full bg-slate-100" aria-hidden="true">
			<svg viewBox="0 0 64 64" class="size-16 text-slate-300" fill="currentColor">
				<circle cx="32" cy="12" r="8" />
				<path d="M20 24h24l10 14-5 3-7-9v28h-7V44h-6v16h-7V32l-7 9-5-3z" />
			</svg>
		</div>
		<h2 class="mt-6 text-lg font-semibold text-slate-900">You haven't been scanned yet</h2>
		<p class="mx-auto mt-2 max-w-md text-sm text-slate-600">
			It takes about 6 minutes with a helper holding the phone. You scan once, and your model is saved until you
			delete it.
		</p>
		<a
			href="/capture"
			class="mt-6 inline-flex rounded-lg bg-indigo-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-indigo-500"
			>Start capture</a
		>
	</section>

	<p class="mt-6 text-xs text-slate-500">ⓘ {DISCLAIMERS.model}</p>
</main>
