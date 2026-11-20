<script lang="ts">
	import type { Snippet } from 'svelte';

	interface Props {
		open: boolean;
		title: string;
		onclose: () => void;
		children: Snippet;
		actions: Snippet;
	}

	let { open, title, onclose, children, actions }: Props = $props();
	let dialog: HTMLDialogElement | undefined = $state();

	// Native <dialog>: focus trap, Esc to close and an accessible modal role for free.
	$effect(() => {
		if (!dialog) return;
		if (open && !dialog.open) dialog.showModal();
		if (!open && dialog.open) dialog.close();
	});
</script>

<dialog
	bind:this={dialog}
	aria-labelledby="modal-title"
	onclose={onclose}
	class="m-auto w-[min(32rem,calc(100vw-2rem))] rounded-2xl border border-slate-200 p-0 shadow-xl backdrop:bg-slate-900/40"
>
	<div class="p-6">
		<h2 id="modal-title" class="text-lg font-semibold text-slate-950">{title}</h2>
		<div class="mt-3 text-sm text-slate-700">{@render children()}</div>
		<div class="mt-6 flex flex-wrap justify-end gap-3">{@render actions()}</div>
	</div>
</dialog>
