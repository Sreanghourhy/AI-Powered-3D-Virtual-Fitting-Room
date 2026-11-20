<script lang="ts">
	import { DISCLAIMERS } from '#lib/components/ui/disclaimers.ts';
	import ModelViewer from './ModelViewer.svelte';
	import type { ModelState } from './model-state.ts';

	let { state }: { state: ModelState } = $props();
</script>

<section
	class="relative h-[60vh] min-h-80 overflow-hidden rounded-2xl border border-slate-200 bg-gradient-to-b from-slate-50 to-slate-200 lg:h-[calc(100vh-7rem)]"
	aria-label="3D model"
>
	{#if state.kind === 'ready'}
		<p class="absolute inset-x-3 top-3 z-10 rounded-lg bg-white/90 px-3 py-2 text-xs font-medium text-slate-700 shadow-sm">
			ⓘ {DISCLAIMERS.tryOn}
		</p>
		<ModelViewer url={state.modelUrl} />
		<p class="absolute inset-x-3 bottom-3 z-10 rounded-lg bg-white/90 px-3 py-2 text-xs text-slate-600 shadow-sm">
			ⓘ {DISCLAIMERS.model}
		</p>
	{:else}
		<div class="grid h-full place-items-center p-6 text-center">
			{#if state.kind === 'none'}
				<div>
					<div class="mx-auto grid size-24 place-items-center rounded-full border-2 border-dashed border-slate-300" aria-hidden="true">
						<svg viewBox="0 0 24 24" class="size-10 text-slate-400" fill="none" stroke="currentColor" stroke-width="1.5">
							<path d="M3 7V5a2 2 0 0 1 2-2h2M17 3h2a2 2 0 0 1 2 2v2M21 17v2a2 2 0 0 1-2 2h-2M7 21H5a2 2 0 0 1-2-2v-2" />
							<circle cx="12" cy="12" r="3.5" />
						</svg>
					</div>
					<h1 class="mt-5 text-xl font-semibold text-slate-900">No scan yet</h1>
					<p class="mx-auto mt-2 max-w-sm text-sm text-slate-600">
						Scan yourself with your MacBook camera to build a 3D model of you. About 4 minutes, on your own.
					</p>
					<a
						href="/scan"
						class="mt-6 inline-flex rounded-lg bg-indigo-600 px-6 py-3 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500"
						>Start Scan</a
					>
				</div>
			{:else if state.kind === 'generating'}
				<div class="w-full max-w-sm">
					<h1 class="text-lg font-semibold text-slate-900">Building your 3D model…</h1>
					<div class="mt-4 h-2 overflow-hidden rounded-full bg-slate-200" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow={state.progress}>
						<div class="h-full bg-indigo-600 transition-all" style:width="{state.progress}%"></div>
					</div>
					<p class="mt-2 text-sm text-slate-600">{state.progress}%{state.step ? ` · ${state.step}` : ''}</p>
					<p class="mt-4 text-xs text-slate-500">This can take several minutes.</p>
				</div>
			{:else if state.kind === 'failed'}
				<div class="max-w-sm" role="alert">
					<h1 class="text-lg font-semibold text-slate-900">We couldn't build a reliable 3D model from this scan</h1>
					<p class="mt-2 text-sm text-slate-600">{state.reason}</p>
					<a href="/scan" class="mt-5 inline-flex rounded-lg bg-indigo-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-indigo-500">Rescan</a>
				</div>
			{/if}
		</div>
	{/if}
</section>
