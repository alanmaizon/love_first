import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../AuthContext';

const Success = () => {
  const { token } = useAuth();
  const [donation, setDonation] = useState(null);

  useEffect(() => {
    axios.get("http://localhost:8000/api/donations/latest/", {
      headers: { Authorization: `Bearer ${token}` }
    })
    .then(response => setDonation(response.data))
    .catch(error => {
      console.error("Error fetching donation details:", error);
      setDonation(null);
    });
  }, [token]);    

  return (
    <div>
      <h1>Thank you for your donation! 🎉</h1>
      {donation && (
        <div>
          <p>Amount: ${donation.amount}</p>
          <p>Date: {new Date(donation.created_at).toLocaleString()}</p>
          {donation.message && <p>Message: {donation.message}</p>}
        </div>
      )}
    </div>
  );
};

export default Success;
