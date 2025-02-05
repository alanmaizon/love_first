import React, { useState, useEffect } from 'react';

const DonationForm = () => {
  const [amount, setAmount] = useState('');
  const [charities, setCharities] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Fetch charities or perform other side effects here
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      // Payment initiation logic here
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
            // Add onChange handler if needed
          />
          {charity.name}
        </label>
      ))}

      <button onClick={handleSubmit} disabled={loading}>
        {loading ? 'Processing...' : 'Donate'}
      </button>
    </div>
  );
};

export default DonationForm;