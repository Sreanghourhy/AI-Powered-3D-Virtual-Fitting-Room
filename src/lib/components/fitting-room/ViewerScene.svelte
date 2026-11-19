<script lang="ts">
	import { T } from '@threlte/core';
	import { OrbitControls } from '@threlte/extras';
	import type { Object3D } from 'three';

	interface Props {
		model: Object3D | null;
		/** Model height in scene units (metres for real scans). */
		height: number;
		autoRotate: boolean;
	}

	let { model, height, autoRotate }: Props = $props();

	// Frame the whole body: look at mid-torso from a few body-heights away.
	const target = $derived<[number, number, number]>([0, height * 0.5, 0]);
	const cameraPosition = $derived<[number, number, number]>([0, height * 0.6, height * 2.6]);
</script>

<T.PerspectiveCamera makeDefault position={cameraPosition} fov={35} near={0.01} far={100}>
	<OrbitControls
		{target}
		{autoRotate}
		autoRotateSpeed={1.5}
		enableDamping
		enablePan={false}
		minDistance={height * 0.6}
		maxDistance={height * 5}
		maxPolarAngle={Math.PI * 0.55}
	/>
</T.PerspectiveCamera>

<T.HemisphereLight args={['#ffffff', '#94a3b8', 1.6]} />
<T.DirectionalLight position={[3, 5, 4]} intensity={2.2} />
<T.DirectionalLight position={[-3, 3, -4]} intensity={0.9} />

<!-- Floor disc -->
<T.Mesh rotation.x={-Math.PI / 2} position.y={-0.001}>
	<T.CircleGeometry args={[height * 0.7, 64]} />
	<T.MeshStandardMaterial color="#e2e8f0" />
</T.Mesh>

{#if model}
	<T is={model} />
{/if}
