<script lang="ts">
	import { goto, invalidateAll } from '$app/navigation';
	import { page } from '$app/state';
	import { ApiError, login, signup } from '#lib/api/client.ts';
	import { safeRedirect } from '#lib/utils/redirect.ts';

	let { mode }: { mode: 'login' | 'signup' } = $props();

	const PASSWORD_MIN = 10;

	let email = $state('');
	let password = $state('');
	let showPassword = $state(false);
	let submitting = $state(false);
	let error = $state<string | null>(null);

	const isSignup = $derived(mode === 'signup');
	const redirectTo = $derived(page.url.searchParams.get('redirectTo'));
	const otherHref = $derived(
		`${isSignup ? '/login' : '/signup'}${redirectTo ? `?redirectTo=${encodeURIComponent(redirectTo)}` : ''}`
	);

	async function submit(event: SubmitEvent) {
		event.preventDefault();
		error = null;
		if (isSignup && password.length < PASSWORD_MIN) {
			error = `Password must be at least ${PASSWORD_MIN} characters.`;
			return;
		}
		submitting = true;
		try {
			await (isSignup ? signup : login)({ email, password });
			await invalidateAll();
			// New accounts go to consent first (docs/user-flows.md, Flow 1).
			await goto(safeRedirect(redirectTo, isSignup ? '/consent' : '/my-model'), { replaceState: true });
		} catch (e) {
			error = e instanceof ApiError ? e.message : 'Something went wrong. Please try again.';
		} finally {
			submitting = false;
		}
	}
</script>

<div class="mx-auto w-full max-w-sm px-4 py-12 sm:py-20">
	<h1 class="text-2xl font-bold tracking-tight text-slate-950">
		{isSignup ? 'Create your account' : 'Sign in'}
	</h1>
	<p class="mt-2 text-sm text-slate-600">
		{isSignup ? 'Scan once and try on clothes on your own 3D model.' : 'Welcome back.'}
	</p>

	<form class="mt-8 space-y-5" onsubmit={submit} novalidate>
		<div>
			<label for="email" class="block text-sm font-medium text-slate-800">Email</label>
			<input
				id="email"
				type="email"
				autocomplete="email"
				required
				bind:value={email}
				class="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 focus:outline-none"
			/>
		</div>

		<div>
			<div class="flex items-center justify-between">
				<label for="password" class="block text-sm font-medium text-slate-800">Password</label>
				<button
					type="button"
					class="text-xs font-medium text-indigo-600 hover:underline"
					aria-controls="password"
					onclick={() => (showPassword = !showPassword)}>{showPassword ? 'Hide' : 'Show'}</button
				>
			</div>
			<input
				id="password"
				type={showPassword ? 'text' : 'password'}
				autocomplete={isSignup ? 'new-password' : 'current-password'}
				required
				minlength={isSignup ? PASSWORD_MIN : undefined}
				aria-describedby={isSignup ? 'password-hint' : undefined}
				bind:value={password}
				class="mt-1 block w-full rounded-lg border border-slate-300 px-3 py-2 text-slate-900 shadow-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 focus:outline-none"
			/>
			{#if isSignup}
				<p id="password-hint" class="mt-1 text-xs text-slate-500">At least {PASSWORD_MIN} characters.</p>
			{/if}
		</div>

		{#if error}
			<p class="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700" role="alert">{error}</p>
		{/if}

		<button
			type="submit"
			disabled={submitting || !email || !password}
			class="w-full rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
		>
			{#if submitting}{isSignup ? 'Creating account…' : 'Signing in…'}{:else}{isSignup ? 'Create account' : 'Sign in'}{/if}
		</button>
	</form>

	<p class="mt-6 text-center text-sm text-slate-600">
		{isSignup ? 'Already have an account?' : 'New here?'}
		<a href={otherHref} class="font-medium text-indigo-600 hover:underline">{isSignup ? 'Sign in' : 'Create an account'}</a>
	</p>
</div>
