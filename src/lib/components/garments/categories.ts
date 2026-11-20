import type { GarmentCategory } from '#lib/types/garment.ts';

/** MVP catalog: shirts and pants only. */
export const CATEGORIES: { id: GarmentCategory; label: string; slot: 'top' | 'bottom' }[] = [
	{ id: 'top', label: 'Shirts', slot: 'top' },
	{ id: 'bottom', label: 'Pants', slot: 'bottom' }
];

export function parseCategory(value: string | null): GarmentCategory {
	return value === 'bottom' ? 'bottom' : 'top';
}
