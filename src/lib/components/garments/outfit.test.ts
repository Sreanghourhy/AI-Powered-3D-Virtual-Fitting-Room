import { describe, expect, it } from 'vitest';
import type { Garment } from '#lib/types/garment.ts';
import { outfitFromParams, outfitQuery } from './outfit.ts';

const garment = (id: string, category: 'top' | 'bottom'): Garment => ({
	id,
	name: id,
	category,
	modelUrl: `/garments/${id}.glb`,
	thumbnailUrl: `/garments/${id}.svg`,
	source: { author: 'x', license: 'x' },
	active: true
});
const catalog = [garment('tee', 'top'), garment('jeans', 'bottom')];

describe('outfitFromParams', () => {
	it('reads both slots independently', () => {
		expect(outfitFromParams(new URLSearchParams('top=tee&bottom=jeans'), catalog)).toEqual({
			topId: 'tee',
			bottomId: 'jeans'
		});
		expect(outfitFromParams(new URLSearchParams('bottom=jeans'), catalog)).toEqual({ topId: null, bottomId: 'jeans' });
	});
	it('ignores unknown ids and wrong-slot ids', () => {
		expect(outfitFromParams(new URLSearchParams('top=jeans&bottom=nope'), catalog)).toEqual({
			topId: null,
			bottomId: null
		});
	});
});

describe('outfitQuery', () => {
	it('omits empty slots', () => {
		expect(outfitQuery({ topId: 'tee', bottomId: null })).toBe('?top=tee');
		expect(outfitQuery({ topId: null, bottomId: null })).toBe('');
	});
});
