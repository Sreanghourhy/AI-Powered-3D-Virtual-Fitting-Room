<script lang="ts">
	import { goto, invalidateAll } from '$app/navigation';
	import { page } from '$app/state';
	import { logout } from '#lib/api/client.ts';
	import type { User } from '#lib/types/api.ts';

	let { user }: { user: User | null } = $props();

	const links = [
		{ href: '/catalog', label: 'Catalog' },
		{ href: '/try-on', label: 'Try-On' },
		{ href: '/my-model', label: 'My Model' }
	];

	let menuOpen = $state(false);
	let accountOpen = $state(false);
	let signingOut = $state(false);

	const isActive = (href: string) => page.url.pathname === href || page.url.pathname.startsWith(`${href}/`);

	// Close menus whenever the route changes.
	$effect(() => {
		void page.url.pathname;
		menuOpen = false;
		accountOpen = false;
	});

	async function signOut() {
		signingOut = true;
		try {
			await logout();
		} catch {
			// Already signed out or backend down; continue to clear the UI.
		}
		await invalidateAll();
		signingOut = false;
		await goto('/');
	}
</script>

<header class="sticky top-0 z-30 border-b border-slate-200 bg-white/90 backdrop-blur">
	<div class="mx-auto flex h-14 max-w-6xl items-center justify-between gap-4 px-4 sm:px-6">
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

		<div class="relative">
			{#if user}
				<button
					type="button"
					class="flex items-center gap-2 rounded-full border border-slate-200 py-1 pr-3 pl-1 text-sm text-slate-700 hover:bg-slate-50"
					aria-haspopup="menu"
					aria-expanded={accountOpen}
					onclick={() => (accountOpen = !accountOpen)}
				>
					<span class="grid size-7 place-items-center rounded-full bg-indigo-600 text-xs font-semibold text-white uppercase">
						{user.email[0]}
					</span>
					<span class="hidden max-w-40 truncate sm:inline">{user.email}</span>
				</button>
				{#if accountOpen}
					<div
						class="absolute right-0 mt-2 w-56 rounded-xl border border-slate-200 bg-white p-1 text-sm shadow-lg"
						role="menu"
					>
						<p class="truncate px-3 py-2 text-xs text-slate-500">{user.email}</p>
						<a href="/my-model" class="block rounded-md px-3 py-2 text-slate-700 hover:bg-slate-100" role="menuitem">My 3D model</a>
						<a href="/consent" class="block rounded-md px-3 py-2 text-slate-700 hover:bg-slate-100" role="menuitem">Privacy & consent</a>
						<button
							type="button"
							class="block w-full rounded-md px-3 py-2 text-left text-slate-700 hover:bg-slate-100 disabled:opacity-50"
							role="menuitem"
							disabled={signingOut}
							onclick={signOut}>{signingOut ? 'Signing out…' : 'Sign out'}</button
						>
					</div>
				{/if}
			{:else}
				<div class="flex items-center gap-2 text-sm">
					<a href="/login" class="rounded-md px-3 py-2 font-medium text-slate-700 hover:bg-slate-100">Sign in</a>
					<a href="/signup" class="rounded-md bg-indigo-600 px-3 py-2 font-semibold text-white hover:bg-indigo-500">Get started</a>
				</div>
			{/if}
		</div>
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
