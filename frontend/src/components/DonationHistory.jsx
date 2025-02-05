import React, { useEffect, useState } from "react";
import axios from "axios";

const API_URL = "http://localhost:8000/api";

const DonationHistory = ({ token }) => {
  const [donations, setDonations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`${API_URL}/donations/`, {
      headers: { Authorization: `Bearer ${token}` },
    })
    .then((response) => {
      setDonations(response.data.results);
      setLoading(false);
    })
    .catch(() => setLoading(false));
  }, []);

  return (
    <div className="donation-history">
      <h2>Your Past Donations</h2>
      {loading ? <p>Loading...</p> : (
        <ul>
          {donations.map((donation) => (
            <li key={donation.id}>
              ${donation.amount} donated on {new Date(donation.created_at).toLocaleDateString()}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default DonationHistory;
