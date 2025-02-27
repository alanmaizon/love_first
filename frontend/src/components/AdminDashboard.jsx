import React from 'react';
import { useAuth } from '../AuthContext';
import { useNavigate } from 'react-router-dom';

const AdminDashboard = () => {
  const { isLoggedIn, username } = useAuth();
  const navigate = useNavigate();

  // Optionally, you might check a flag in the auth state (like isAdmin)
  // For this example, we'll assume the couple's account has a username "couple"
  if (!isLoggedIn) {
    navigate("/login");
    return null;
  }

  if (username !== "couple") {
    return (
      <div className="container mt-5">
        <h2>Access Denied</h2>
        <p>You are not authorized to view this page.</p>
      </div>
    );
  }

  return (
    <div className="container mt-5">
      <h1 className="mb-4">Admin Panel (Restricted)</h1>
      <div className="list-group">
        <button
          className="list-group-item list-group-item-action"
          onClick={() => navigate('/admin/donations')}
        >
          View All Donations
        </button>
        <button
          className="list-group-item list-group-item-action"
          onClick={() => navigate('/admin/confirm-donations')}
        >
          Confirm Donations (Mark as Received)
        </button>
        <button
          className="list-group-item list-group-item-action"
          onClick={() => navigate('/admin/charities')}
        >
          Manage Charities (Add/Edit/Delete)
        </button>
        <button
          className="list-group-item list-group-item-action"
          onClick={() => navigate('/admin/stats')}
        >
          View Stats: Total Donations, Top Contributors
        </button>
      </div>
    </div>
  );
};

export default AdminDashboard;
