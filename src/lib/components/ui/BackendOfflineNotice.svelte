<script lang="ts">
	let { message }: { message: string } = $props();
</script>

<div class="rounded-xl border border-amber-300 bg-amber-50 px-4 py-3 text-sm text-amber-900" role="alert">
	<strong>Backend offline.</strong>
	{message}
</div>
