<script lang="ts">
	import './layout.css';
	import favicon from '#lib/assets/favicon.svg';
	import AppHeader from '#lib/components/ui/AppHeader.svelte';
	import type { LayoutProps } from './$types';

	let { children, data }: LayoutProps = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<div class="flex min-h-screen flex-col bg-white">
	<AppHeader user={data.user} />
	<div class="flex-1">
		{@render children()}
	</div>
</div>
