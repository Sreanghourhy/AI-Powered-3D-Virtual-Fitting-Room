import { describe, expect, it } from 'vitest';
import { getFlag, setFlag } from './local-flag.ts';

class MemoryStorage implements Storage {
	private data = new Map<string, string>();
	get length() {
		return this.data.size;
	}
	clear() {
		this.data.clear();
	}
	getItem(key: string) {
		return this.data.get(key) ?? null;
	}
	key(index: number) {
		return [...this.data.keys()][index] ?? null;
	}
	removeItem(key: string) {
		this.data.delete(key);
	}
	setItem(key: string, value: string) {
		this.data.set(key, value);
	}
}

const throwing = {
	getItem() {
		throw new Error('blocked');
	},
	setItem() {
		throw new Error('blocked');
	},
	removeItem() {
		throw new Error('blocked');
	}
} as unknown as Storage;

describe('local flags', () => {
	it('sets, reads and clears a flag', () => {
		const storage = new MemoryStorage();
		expect(getFlag('x', storage)).toBe(false);
		setFlag('x', true, storage);
		expect(getFlag('x', storage)).toBe(true);
		setFlag('x', false, storage);
		expect(getFlag('x', storage)).toBe(false);
	});

	it('never throws when storage is blocked or missing', () => {
		expect(getFlag('x', throwing)).toBe(false);
		expect(() => setFlag('x', true, throwing)).not.toThrow();
		expect(getFlag('x', undefined)).toBe(false);
	});
});
