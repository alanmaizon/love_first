import React, { useState, useEffect } from "react";
import { useAuth } from "../AuthContext";

const DonationForm = () => {
  const [amount, setAmount] = useState("");
  const [charities, setCharities] = useState([]);
  const [selectedCharities, setSelectedCharities] = useState([]);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { token } = useAuth();

  useEffect(() => {
    fetch("http://localhost:8000/api/charities/")
      .then((res) => res.json())
      .then((data) => setCharities(data.results))
      .catch(() => setError("Failed to load charities"));
  }, []);

  const handleCharitySelection = (charityId) => {
    setSelectedCharities((prev) =>
      prev.includes(charityId)
        ? prev.filter((id) => id !== charityId)
        : [...prev, charityId]
    );
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    if (!amount || selectedCharities.length === 0) {
      setError("Please enter an amount and select at least one charity.");
      setLoading(false);
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/api/donations/", {
        method: "POST",
        headers: { 
          "Content-Type": "application/json", 
          Authorization: `Bearer ${token}` 
        },
        body: JSON.stringify({
          amount, 
          charities: selectedCharities, 
          payment_method: "manual",
          message,
        }),
      });

      if (!response.ok) throw new Error("Failed to submit donation");

      window.location.href = "/success";
    } catch (err) {
      setError("Donation submission failed. Try again.");
    }

    setLoading(false);
  };

  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <div className="card shadow p-4">
            <h2 className="card-title text-center mb-4">Make a Donation</h2>
            {error && <div className="alert alert-danger">{error}</div>}
            <form onSubmit={handleSubmit}>
              <div className="mb-3">
                <label htmlFor="amount" className="form-label">
                  Donation Amount ($)
                </label>
                <input
                  type="number"
                  id="amount"
                  className="form-control"
                  placeholder="Enter amount"
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                />
              </div>
              <div className="mb-3">
                <label htmlFor="message" className="form-label">
                  Personalized Message (Optional)
                </label>
                <textarea
                  id="message"
                  className="form-control"
                  placeholder="Leave a dedication message..."
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                ></textarea>
              </div>
              <div className="mb-3">
                <h5>Select Charities:</h5>
                {charities.map((charity) => (
                  <div className="form-check" key={charity.id}>
                    <input
                      className="form-check-input"
                      type="checkbox"
                      value={charity.id}
                      checked={selectedCharities.includes(charity.id)}
                      onChange={() => handleCharitySelection(charity.id)}
                      id={`charity-${charity.id}`}
                    />
                    <label
                      className="form-check-label"
                      htmlFor={`charity-${charity.id}`}
                    >
                      {charity.name}
                    </label>
                  </div>
                ))}
              </div>
              <button type="submit" className="btn btn-primary w-100" disabled={loading}>
                {loading ? "Processing..." : "Donate Now"}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DonationForm;
