<!-- Consent text v2 (MacBook camera). Source of truth: docs/consent-v2.md (approved 20 Nov 2026). -->
<script lang="ts">
	const sections: { title: string; open?: boolean; items: string[] }[] = [
		{
			title: 'What we collect',
			open: true,
			items: [
				'Photos of your face and whole body, from several angles',
				'The 3D model we build from them',
				'The clothes you choose to try on'
			]
		},
		{
			title: 'Why',
			items: [
				'Only to show you a 3D try-on preview. We don’t use your photos or model for advertising, sell them, or use them to train AI without asking you separately.'
			]
		},
		{
			title: 'How we protect it',
			items: [
				'The camera is only on during the capture steps and turns off when you finish or leave the page.',
				'Nothing is uploaded until you press Upload.',
				'Your photos and model are encrypted and stored privately.',
				'Only you can see your model after signing in.',
				'We remove hidden data (metadata) from your photos.',
				'We delete your original photos once your model is ready. We keep only the 3D model.'
			]
		},
		{
			title: 'How long we keep it',
			open: true,
			items: [
				'Until you delete it. You can delete your 3D model, or your whole account, at any time from My Model or Account.',
				'Deleted data is removed right away from our main storage and within 30 days from backups.'
			]
		},
		{
			title: 'Your choices',
			items: [
				'You can view, download (export), or delete your model at any time.',
				'You can withdraw this consent at any time. We will then delete your scan data.'
			]
		},
		{
			title: 'Important to know',
			items: [
				'The 3D model is an approximation. Hair, loose clothing and hidden areas may not look exactly like you.',
				'We do not change your face or body shape, and we do not replace you with a generic avatar.',
				'The try-on is a visual preview only. It does not tell you your exact size or how the clothes will really fit.'
			]
		},
		{
			title: 'Who can be scanned',
			items: [
				'You must be 18 or older, and you may scan only yourself, standing in front of your MacBook camera.'
			]
		}
	];
</script>

<p class="text-slate-700">
	We will use your <strong>MacBook's built-in camera</strong> to take photos of you from the front, sides and back,
	plus a few close-ups of your face. Our system turns these photos into a <strong>3D model of you</strong> so you can
	try on clothes.
</p>

<div class="mt-6 divide-y divide-slate-200 rounded-xl border border-slate-200">
	{#each sections as section (section.title)}
		<details class="group px-4 py-3" open={section.open}>
			<summary class="flex cursor-pointer list-none items-center justify-between font-medium text-slate-900">
				{section.title}
				<span class="text-slate-400 transition group-open:rotate-45" aria-hidden="true">+</span>
			</summary>
			<ul class="mt-2 list-disc space-y-1 pl-5 text-sm text-slate-600">
				{#each section.items as item (item)}
					<li>{item}</li>
				{/each}
			</ul>
		</details>
	{/each}
</div>
