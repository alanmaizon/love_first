import React, { useEffect, useState } from "react";
import axios from "axios";
import { useAuth } from "../AuthContext";

const API_URL = "http://localhost:8000/api";

const DonationHistory = () => {
  const { token } = useAuth();
  const [donations, setDonations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!token) return;
    
    axios
      .get(`${API_URL}/donations/`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((response) => {
        // Handle both paginated and non-paginated responses.
        const data = response.data.results || response.data;
        setDonations(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching donations:", err);
        setError("Failed to fetch donations. Please try again later.");
        setLoading(false);
      });
  }, [token]);

  if (loading) return <p>Loading donations...</p>;
  if (error) return <p>{error}</p>;
  if (donations.length === 0) return <p>No donations found.</p>;

  return (
    <div className="donation-history">
      <h2>Your Past Donations</h2>
      <div className="row">
        {donations.map((donation) => (
          <div key={donation.id} className="col-md-6 mb-3">
            <div className="card h-100">
              <div className="card-body">
                <h5 className="card-title">${donation.amount} donated</h5>
                <p className="card-text">
                  <strong>Date:</strong>{" "}
                  {new Date(donation.created_at).toLocaleString()}
                </p>
                <p className="card-text">
                  <strong>Payment Method:</strong> {donation.payment_method}
                </p>
                {donation.message && (
                  <p className="card-text">
                    <strong>Message:</strong> {donation.message}
                  </p>
                )}
                {donation.charities && donation.charities.length > 0 && (
                  <p className="card-text">
                    <strong>Charities:</strong>{" "}
                    {donation.charities
                      .map((c) =>
                        typeof c === "object" && c.name ? c.name : c
                      )
                      .join(", ")}
                  </p>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DonationHistory;
