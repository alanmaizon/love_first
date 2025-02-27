import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter as Router } from 'react-router-dom';
import { Login } from '../Authentication';
import { useAuth } from '../../AuthContext';
import { login as apiLogin } from '../../services/api';
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

test('allows user to log in successfully', async () => {
  const mockLogin = vi.fn();
  const mockNavigate = vi.fn();
  useAuth.mockReturnValue({ login: mockLogin });
  useNavigate.mockReturnValue(mockNavigate);

  apiLogin.mockResolvedValue({ access: 'access_token', refresh: 'refresh_token' });

  render(
    <Router>
      <Login />
    </Router>
  );

  fireEvent.change(screen.getByPlaceholderText(/Username/i), { target: { value: 'testuser' } });
  fireEvent.change(screen.getByPlaceholderText(/Password/i), { target: { value: 'Test1234!' } });
  fireEvent.click(screen.getByText(/Login/i));

  await waitFor(() => {
    expect(apiLogin).toHaveBeenCalledWith('testuser', 'Test1234!');
    expect(mockLogin).toHaveBeenCalledWith('access_token', 'refresh_token', 'testuser');
    expect(mockNavigate).toHaveBeenCalledWith('/donate');
  });
});

test('shows error message on failed login', async () => {
  apiLogin.mockRejectedValueOnce(new Error('Invalid credentials'));

  render(
    <Router>
      <Login />
    </Router>
  );

  fireEvent.change(screen.getByPlaceholderText(/Username/i), { target: { value: 'wronguser' } });
  fireEvent.change(screen.getByPlaceholderText(/Password/i), { target: { value: 'WrongPass!' } });
  fireEvent.click(screen.getByText(/Login/i));

  const errorMessage = await screen.findByText(/An error occurred/i);
  expect(errorMessage).toBeInTheDocument();
});

// Similar tests for logout, protected routes, and API errors can be added
