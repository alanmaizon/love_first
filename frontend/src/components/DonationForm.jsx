import React, { useState, useEffect } from "react";
import { useAuth } from "../AuthContext"; // Para obtener el token del usuario
import { createStripeCheckout, createPayPalPayment } from "../services/donationService";

const DonationForm = () => {
  const [amount, setAmount] = useState("");
  const [charities, setCharities] = useState([]);
  const [selectedCharities, setSelectedCharities] = useState([]);
  const [paymentMethod, setPaymentMethod] = useState("stripe");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { token } = useAuth(); // Obtener el token del usuario
  console.log("Auth Token:", token);

  useEffect(() => {
    // Obtener las organizaciones benéficas disponibles desde el backend
    fetch("http://localhost:8000/api/charities/")
      .then((res) => res.json())
      .then((data) => setCharities(data.results))
      .catch(() => setError("Failed to load charities"));
  }, []);

  const handleCharitySelection = (charityId) => {
    setSelectedCharities((prev) =>
      prev.includes(charityId) ? prev.filter((id) => id !== charityId) : [...prev, charityId]
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
      let response;
      if (paymentMethod === "stripe") {
        response = await createStripeCheckout(amount, selectedCharities, token);
        window.location.href = response.stripe_url; // Redirigir a Stripe
      } else {
        response = await createPayPalPayment(amount, selectedCharities, token);
        window.location.href = response.paypal_url; // Redirigir a PayPal
      }
    } catch (err) {
      setError("Payment initiation failed. Try again.");
    }
    setLoading(false);
  };

  return (
    <div className="donation-form">
      <h2>Make a Donation</h2>

      {error && <p className="error">{error}</p>}

      <input
        type="number"
        placeholder="Enter donation amount"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
      />

      <h4>Select Charities:</h4>
      {charities.map((charity) => (
        <label key={charity.id}>
          <input
            type="checkbox"
            value={charity.id}
            checked={selectedCharities.includes(charity.id)}
            onChange={() => handleCharitySelection(charity.id)}
          />
          {charity.name}
        </label>
      ))}

      <h4>Payment Method:</h4>
      <label>
        <input
          type="radio"
          value="stripe"
          checked={paymentMethod === "stripe"}
          onChange={() => setPaymentMethod("stripe")}
        />
        Stripe
      </label>
      <label>
        <input
          type="radio"
          value="paypal"
          checked={paymentMethod === "paypal"}
          onChange={() => setPaymentMethod("paypal")}
        />
        PayPal
      </label>

      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Processing..." : "Donate"}
      </button>
    </div>
  );
};

export default DonationForm;