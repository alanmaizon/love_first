import '@testing-library/jest-dom';
import { vi } from 'vitest';

global.localStorage = {
  getItem: vi.fn(() => 'mockAccessToken'),
  setItem: vi.fn(),
  removeItem: vi.fn(),
};

beforeEach(() => {
  localStorage.setItem('accessToken', 'mockAccessToken');
});