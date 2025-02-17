import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter as Router } from 'react-router-dom';
import { Register } from '../Authentication';
import { useAuth } from '../../AuthContext';
import { register as apiRegister, login as apiLogin } from '../../services/api';
import { vi } from 'vitest';
import { useNavigate } from 'react-router-dom';

vi.mock('../../AuthContext');
vi.mock('../../services/api');
vi.mock('react-router-dom', async (importOriginal) => {
  const actual = await importOriginal();
  return {
    ...actual,
    useNavigate: vi.fn(),
  };
});

test('renders Signup form and handles input changes', async () => {
  const mockLogin = vi.fn();
  const mockNavigate = vi.fn();
  useAuth.mockReturnValue({ login: mockLogin });
  useNavigate.mockReturnValue(mockNavigate);

  apiRegister.mockResolvedValue({});
  apiLogin.mockResolvedValue({ access: 'access_token', refresh: 'refresh_token' });

  render(
    <Router>
      <Register />
    </Router>
  );

  // Check if input fields exist
  const usernameInput = screen.getByPlaceholderText(/Username/i);
  const emailInput = screen.getByPlaceholderText(/Email/i);
  const passwordInput = screen.getByPlaceholderText(/Password/i);
  const submitButton = screen.getByText(/Register/i);

  expect(usernameInput).toBeInTheDocument();
  expect(emailInput).toBeInTheDocument();
  expect(passwordInput).toBeInTheDocument();
  expect(submitButton).toBeInTheDocument();

  // Simulate user typing
  fireEvent.change(usernameInput, { target: { value: 'testuser' } });
  fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
  fireEvent.change(passwordInput, { target: { value: 'Test1234!' } });

  expect(usernameInput.value).toBe('testuser');
  expect(emailInput.value).toBe('test@example.com');
  expect(passwordInput.value).toBe('Test1234!');

  // Simulate form submission
  fireEvent.click(submitButton);

  // Wait for async operations to complete
  await waitFor(() => {
    expect(apiRegister).toHaveBeenCalledWith('testuser', 'test@example.com', 'Test1234!');
    expect(apiLogin).toHaveBeenCalledWith('testuser', 'Test1234!');
    expect(mockLogin).toHaveBeenCalledWith('access_token', 'refresh_token', 'testuser');
    expect(mockNavigate).toHaveBeenCalledWith('/private');
  });
});