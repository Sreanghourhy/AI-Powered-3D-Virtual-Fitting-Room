<script lang="ts">
	import { page } from '$app/state';

	// Single-user local prototype (CR-02): no account menu, sign-in or profiles.
	const links = [
		{ href: '/', label: 'Fitting room' },
		{ href: '/catalog', label: 'Catalog' }
	];

	let menuOpen = $state(false);

	const isActive = (href: string) =>
		href === '/' ? page.url.pathname === '/' : page.url.pathname === href || page.url.pathname.startsWith(`${href}/`);

	// Close the mobile menu whenever the route changes.
	$effect(() => {
		void page.url.pathname;
		menuOpen = false;
	});
</script>

<header class="sticky top-0 z-30 border-b border-slate-200 bg-white/90 backdrop-blur">
	<div class="mx-auto flex h-14 max-w-7xl items-center justify-between gap-4 px-4 sm:px-6">
		<div class="flex items-center gap-2">
			<button
				type="button"
				class="-ml-2 rounded-md p-2 text-slate-700 hover:bg-slate-100 md:hidden"
				aria-label="Open menu"
				aria-expanded={menuOpen}
				aria-controls="mobile-nav"
				onclick={() => (menuOpen = !menuOpen)}
			>
				<svg class="size-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
					{#if menuOpen}
						<path d="M5.3 4.3a1 1 0 0 1 1.4 0L10 7.6l3.3-3.3a1 1 0 1 1 1.4 1.4L11.4 9l3.3 3.3a1 1 0 0 1-1.4 1.4L10 10.4l-3.3 3.3a1 1 0 0 1-1.4-1.4L8.6 9 5.3 5.7a1 1 0 0 1 0-1.4Z" />
					{:else}
						<path d="M3 5h14a1 1 0 1 0 0-2H3a1 1 0 0 0 0 2Zm14 4H3a1 1 0 0 0 0 2h14a1 1 0 1 0 0-2Zm0 6H3a1 1 0 1 0 0 2h14a1 1 0 1 0 0-2Z" />
					{/if}
				</svg>
			</button>
			<a href="/" class="font-semibold tracking-tight text-slate-950">Fitting Room</a>
		</div>

		<nav class="hidden items-center gap-1 md:flex" aria-label="Main">
			{#each links as link (link.href)}
				<a
					href={link.href}
					class="rounded-md px-3 py-2 text-sm font-medium {isActive(link.href)
						? 'bg-indigo-50 text-indigo-700'
						: 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'}"
					aria-current={isActive(link.href) ? 'page' : undefined}>{link.label}</a
				>
			{/each}
		</nav>
	</div>

	{#if menuOpen}
		<nav id="mobile-nav" class="border-t border-slate-200 px-4 py-2 md:hidden" aria-label="Main">
			{#each links as link (link.href)}
				<a
					href={link.href}
					class="block rounded-md px-3 py-3 text-base font-medium {isActive(link.href)
						? 'bg-indigo-50 text-indigo-700'
						: 'text-slate-700 hover:bg-slate-100'}"
					aria-current={isActive(link.href) ? 'page' : undefined}>{link.label}</a
				>
			{/each}
		</nav>
	{/if}
</header>
