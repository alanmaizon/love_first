import React, { useState } from 'react';

const DonationForm = ({ charities, handleDonation }) => {
  const [donationAmount, setDonationAmount] = useState('');
  const [selectedCharities, setSelectedCharities] = useState([]);

  const handleCharityChange = (event) => {
    const { value, checked } = event.target;
    setSelectedCharities((prev) => 
      checked ? [...prev, value] : prev.filter((charity) => charity !== value)
    );
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    handleDonation(donationAmount, selectedCharities);
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3>Make a Donation</h3>
      <input
        type="number"
        value={donationAmount}
        onChange={(e) => setDonationAmount(e.target.value)}
        placeholder="Donation Amount (€)"
      />
      <div>
        <h4>Select Charities:</h4>
        {charities.map((charity) => (
          <label key={charity.id}>
            <input
              type="checkbox"
              value={charity.id}
              onChange={handleCharityChange}
            />
            {charity.name}
          </label>
        ))}
      </div>
      <button type="submit">Donate</button>
    </form>
  );
};

export default DonationForm;
