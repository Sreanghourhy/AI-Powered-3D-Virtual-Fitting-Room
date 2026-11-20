<script lang="ts">
	import BackendStatus from '#lib/components/ui/BackendStatus.svelte';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();

	const steps = [
		{ title: 'Scan once', text: 'Stand in front of your MacBook camera and turn slowly. About 4 minutes.' },
		{ title: 'Your own 3D model', text: 'We build a model from your real appearance. No avatar editing.' },
		{ title: 'Try on anytime', text: 'Switch shirts and pants on your saved model, until you delete it.' }
	];
</script>

<svelte:head>
	<title>AI-Powered 3D Virtual Fitting Room</title>
	<meta name="description" content="Scan once, then try on shirts and pants on your own 3D model." />
</svelte:head>

<main class="mx-auto max-w-6xl px-4 py-12 sm:px-6 sm:py-20">
	<div class="flex justify-end"><BackendStatus /></div>
	<h1 class="mt-4 max-w-3xl text-4xl font-bold tracking-tight text-slate-950 sm:text-5xl">
		Try on clothes on your own 3D model
	</h1>
	<p class="mt-5 max-w-2xl text-lg text-slate-600">Scan once, save until you delete it, try on clothes anytime.</p>
	<div class="mt-8 flex flex-wrap gap-3">
		{#if data.user}
			<a href="/my-model" class="rounded-lg bg-indigo-600 px-5 py-3 text-sm font-semibold text-white hover:bg-indigo-500">Go to my model</a>
		{:else}
			<a href="/signup" class="rounded-lg bg-indigo-600 px-5 py-3 text-sm font-semibold text-white hover:bg-indigo-500">Get started</a>
		{/if}
		<a href="/catalog" class="rounded-lg border border-slate-300 px-5 py-3 text-sm font-semibold text-slate-800 hover:bg-slate-50">Browse catalog</a>
	</div>

	<ol class="mt-16 grid gap-4 sm:grid-cols-3">
		{#each steps as step, i (step.title)}
			<li class="rounded-2xl border border-slate-200 p-6">
				<p class="text-sm font-semibold text-indigo-600">Step {i + 1}</p>
				<h2 class="mt-2 text-lg font-semibold text-slate-900">{step.title}</h2>
				<p class="mt-2 text-sm text-slate-600">{step.text}</p>
			</li>
		{/each}
	</ol>

	<p class="mt-10 text-xs text-slate-500">
		The try-on is a visual preview only — not a size or fit guarantee.
		<a href="/viewer-demo" class="underline">See the 3D viewer demo</a>.
	</p>
</main>
