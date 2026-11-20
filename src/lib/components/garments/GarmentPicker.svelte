<script lang="ts">
	import type { Garment } from '#lib/types/garment.ts';

	interface Props {
		label: string;
		garments: Garment[];
		selectedId: string | null;
		onselect: (id: string | null) => void;
	}

	let { label, garments, selectedId, onselect }: Props = $props();

	const selected = $derived(garments.find((g) => g.id === selectedId));
	const groupId = $derived(`picker-${label.toLowerCase()}`);
</script>

<fieldset>
	<div class="flex items-baseline justify-between">
		<legend id={groupId} class="text-sm font-semibold text-slate-900">{label}</legend>
		<span class="text-xs text-slate-500">{selected ? selected.name : 'None'}</span>
	</div>
	<div class="mt-2 flex gap-2 overflow-x-auto pb-1" role="radiogroup" aria-labelledby={groupId}>
		<button
			type="button"
			role="radio"
			aria-checked={selectedId === null}
			aria-label="No {label.toLowerCase()}"
			onclick={() => onselect(null)}
			class="grid size-16 shrink-0 place-items-center rounded-xl border-2 bg-white text-xl text-slate-400 {selectedId === null
				? 'border-indigo-600'
				: 'border-slate-200 hover:border-slate-300'}">∅</button
		>
		{#each garments as garment (garment.id)}
			<button
				type="button"
				role="radio"
				aria-checked={selectedId === garment.id}
				aria-label={garment.name}
				title={garment.name}
				onclick={() => onselect(garment.id)}
				class="size-16 shrink-0 overflow-hidden rounded-xl border-2 bg-slate-100 {selectedId === garment.id
					? 'border-indigo-600'
					: 'border-slate-200 hover:border-slate-300'}"
			>
				<img src={garment.thumbnailUrl} alt="" class="size-full object-contain" />
			</button>
		{/each}
	</div>
</fieldset>
