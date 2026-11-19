/**
 * Garment data model. Spec: docs/garment-format.md
 * MVP supports shirts ("top") and pants ("bottom") only.
 */
export type GarmentCategory = 'top' | 'bottom';

export interface GarmentSource {
	author: string;
	/** SPDX license id (e.g. "CC-BY-4.0") or "proprietary". */
	license: string;
	url?: string;
}

export interface Garment {
	/** Stable kebab-case id, e.g. "shirt-basic-tee-white". */
	id: string;
	name: string;
	category: GarmentCategory;
	/** GLB file: metres, Y-up, faces +Z, origin at floor. */
	modelUrl: string;
	/** 512×512 front-view thumbnail. */
	thumbnailUrl: string;
	/** Optional hex colours for filtering. */
	colors?: string[];
	/** Display only — not used for fit in the MVP. */
	sizes?: string[];
	source: GarmentSource;
	active: boolean;
}

/** One shirt + one pants selection; either slot may be empty. */
export interface Outfit {
	topId: string | null;
	bottomId: string | null;
}
