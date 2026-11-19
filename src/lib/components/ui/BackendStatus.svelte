<script lang="ts">
	import { onMount } from 'svelte';
	import { getHealth } from '#lib/api/client.ts';

	let status = $state<'checking' | 'ok' | 'offline'>('checking');

	onMount(() => {
		getHealth()
			.then(() => (status = 'ok'))
			.catch(() => (status = 'offline'));
	});

	const styles = {
		checking: 'bg-slate-100 text-slate-600',
		ok: 'bg-emerald-50 text-emerald-700',
		offline: 'bg-amber-50 text-amber-800'
	};
	const labels = { checking: 'checking…', ok: 'ok', offline: 'offline' };
</script>

<span class="inline-flex items-center gap-2 rounded-full px-3 py-1 text-xs font-medium {styles[status]}">
	<span
		class="size-2 rounded-full {status === 'ok'
			? 'bg-emerald-500'
			: status === 'offline'
				? 'bg-amber-500'
				: 'bg-slate-400'}"
	></span>
	Backend: {labels[status]}
</span>
