import type { Garment, Outfit } from '#lib/types/garment.ts';

/** Read the outfit from ?top=&bottom=, ignoring ids that aren't in the right category. */
export function outfitFromParams(params: Pick<URLSearchParams, 'get'>, garments: Garment[]): Outfit {
	const pick = (slot: 'top' | 'bottom') => {
		const id = params.get(slot);
		return garments.some((g) => g.id === id && g.category === slot) ? id : null;
	};
	return { topId: pick('top'), bottomId: pick('bottom') };
}

/** Query string for an outfit (empty slots omitted). */
export function outfitQuery(outfit: Outfit): string {
	const params = new URLSearchParams();
	if (outfit.topId) params.set('top', outfit.topId);
	if (outfit.bottomId) params.set('bottom', outfit.bottomId);
	const query = params.toString();
	return query ? `?${query}` : '';
}
