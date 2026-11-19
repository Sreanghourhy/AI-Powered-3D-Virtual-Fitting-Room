<script lang="ts">
	import { Canvas } from '@threlte/core';
	import { Box3, Mesh, Vector3, type Material, type Object3D } from 'three';
	import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
	import ViewerScene from './ViewerScene.svelte';

	interface Props {
		/** URL of a GLB/glTF file. */
		url: string;
		/** Slowly spin the model when the user is not interacting. */
		autoRotate?: boolean;
	}

	let { url, autoRotate = false }: Props = $props();

	let model = $state.raw<Object3D | null>(null);
	let height = $state(1.7);
	let status = $state<'loading' | 'ready' | 'error'>('loading');

	/** Centre the model on X/Z, put its feet at y = 0, and return its height. */
	function normalize(root: Object3D): number {
		root.updateMatrixWorld(true);
		const box = new Box3().setFromObject(root);
		const center = box.getCenter(new Vector3());
		root.position.x -= center.x;
		root.position.z -= center.z;
		root.position.y -= box.min.y;
		const h = box.max.y - box.min.y;
		return h > 0 ? h : 1.7;
	}

	function dispose(root: Object3D) {
		root.traverse((obj) => {
			if (obj instanceof Mesh) {
				obj.geometry.dispose();
				const materials: Material[] = Array.isArray(obj.material) ? obj.material : [obj.material];
				materials.forEach((m) => m.dispose());
			}
		});
	}

	$effect(() => {
		const current = url;
		let cancelled = false;
		status = 'loading';

		new GLTFLoader()
			.loadAsync(current)
			.then((gltf) => {
				if (cancelled) {
					dispose(gltf.scene);
					return;
				}
				height = normalize(gltf.scene);
				model = gltf.scene;
				status = 'ready';
			})
			.catch((err) => {
				if (cancelled) return;
				console.error('Failed to load model', err);
				status = 'error';
			});

		return () => {
			cancelled = true;
			if (model) {
				dispose(model);
				model = null;
			}
		};
	});
</script>

<div class="relative h-full w-full touch-none select-none">
	<Canvas>
		<ViewerScene {model} {height} {autoRotate} />
	</Canvas>

	{#if status === 'loading'}
		<div class="pointer-events-none absolute inset-0 grid place-items-center">
			<p class="rounded-full bg-white/80 px-4 py-2 text-sm text-slate-600 shadow">Loading 3D model…</p>
		</div>
	{:else if status === 'error'}
		<div class="absolute inset-0 grid place-items-center">
			<p class="rounded-lg bg-red-50 px-4 py-2 text-sm text-red-700 shadow" role="alert">
				Could not load the 3D model.
			</p>
		</div>
	{/if}
</div>
