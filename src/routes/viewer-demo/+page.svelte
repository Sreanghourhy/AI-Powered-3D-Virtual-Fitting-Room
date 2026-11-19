<script lang="ts">
	import ModelViewer from '#lib/components/fitting-room/ModelViewer.svelte';

	let autoRotate = $state(true);
</script>

<svelte:head>
	<title>3D Viewer Demo · Virtual Fitting Room</title>
</svelte:head>

<main class="mx-auto flex min-h-screen max-w-5xl flex-col px-4 py-8 sm:px-6">
	<header class="mb-4 flex flex-wrap items-end justify-between gap-3">
		<div>
			<a href="/" class="text-sm text-indigo-600 hover:underline">← Home</a>
			<h1 class="mt-1 text-2xl font-bold text-slate-950">3D viewer demo</h1>
			<p class="text-sm text-slate-600">Drag to rotate 360°, scroll or pinch to zoom.</p>
		</div>
		<label class="flex items-center gap-2 text-sm text-slate-700">
			<input type="checkbox" bind:checked={autoRotate} class="size-4 accent-indigo-600" />
			Auto-rotate
		</label>
	</header>

	<div class="h-[70vh] min-h-96 overflow-hidden rounded-2xl border border-slate-200 bg-gradient-to-b from-slate-50 to-slate-200">
		<ModelViewer url="/models/sample.glb" {autoRotate} />
	</div>

	<p class="mt-3 text-xs text-slate-500">
		Sample model: “Cesium Man” © 2017 Cesium, licensed
		<a class="underline" href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noreferrer">CC BY 4.0</a>.
		Public sample only. No customer data is shown on this page.
	</p>
</main>
