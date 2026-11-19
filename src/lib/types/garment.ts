export interface Garment {
	id: string;
	name: string;
	category: 'top' | 'bottom' | 'dress' | 'outerwear';
	modelUrl?: string;
	thumbnailUrl?: string;
}
