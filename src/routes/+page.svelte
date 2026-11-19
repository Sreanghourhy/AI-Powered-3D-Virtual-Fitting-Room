<script lang="ts">
	import FittingRoomPlaceholder from '#lib/components/fitting-room/FittingRoomPlaceholder.svelte';
</script>

<svelte:head>
	<title>AI-Powered 3D Virtual Fitting Room</title>
	<meta name="description" content="A starter project for an AI-powered 3D virtual fitting room." />
</svelte:head>

<main class="mx-auto min-h-screen max-w-5xl px-6 py-16 sm:py-24">
	<header class="mb-12">
		<p class="text-sm font-semibold uppercase tracking-widest text-indigo-600">Project starter</p>
		<h1 class="mt-4 max-w-3xl text-4xl font-bold tracking-tight text-slate-950 sm:text-5xl">AI-Powered 3D Virtual Fitting Room</h1>
		<p class="mt-5 text-lg text-slate-600">Built with SvelteKit, TypeScript, and Tailwind CSS.</p>
	</header>
	<FittingRoomPlaceholder />
</main>
