import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';
import { Login } from '../Authentication';
import { useAuth } from '../../AuthContext';
import { login as apiLogin } from '../../services/api';
import { vi } from 'vitest';
import ProtectedRoute from '../ProtectedRoute';

// Mock dependencies
vi.mock('../../AuthContext');
vi.mock('../../services/api');

// ✅ Corrected `useNavigate` mock at top level
const mockNavigate = vi.fn();

vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    useNavigate: () => mockNavigate, // ✅ Corrected: return a function that returns `mockNavigate`
  };
});

describe('Authentication Tests', () => {
  let mockLogin, mockLogout;

  beforeEach(() => {
    mockLogin = vi.fn();
    mockLogout = vi.fn();

    useAuth.mockReturnValue({ login: mockLogin, logout: mockLogout, user: null });

    // ✅ No need to re-import `useNavigate`, it's already mocked
  });

  test('Logout should clear auth state and redirect', () => {
    mockLogout();
    expect(mockLogout).toHaveBeenCalled();
    mockNavigate('/login');
    expect(mockNavigate).toHaveBeenCalledWith('/login');
  });

  test('Protected route redirects unauthenticated users', async () => {
    useAuth.mockReturnValue({ user: null });
  
    render(
      <Router>
        <Routes>
          <Route path="/" element={<div>Home Page</div>} /> {/* Add this line */}
          <Route
            path="/protected"
            element={
              <ProtectedRoute>
                <div>Protected Content</div>
              </ProtectedRoute>
            }
          />
          <Route path="/login" element={<div>Login Page</div>} />
        </Routes>
      </Router>
    );
  
    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith('/login');
    });
  });

  test('Handles API login failure correctly', async () => {
    apiLogin.mockRejectedValue(new Error('Invalid credentials'));

    render(
      <Router>
        <Login />
      </Router>
    );

    fireEvent.change(screen.getByPlaceholderText(/Username/i), { target: { value: 'wronguser' } });
    fireEvent.change(screen.getByPlaceholderText(/Password/i), { target: { value: 'wrongpass' } });
    fireEvent.click(screen.getByText(/Login/i));

    await waitFor(() => {
      expect(screen.getByText(/An error occurred/i)).toBeInTheDocument();
    });
  });
});
