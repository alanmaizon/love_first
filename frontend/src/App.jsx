import React, { useState, useEffect } from "react";
import DonationForm from "./components/DonationForm";
import { submitDonation } from "./api/donations";

function App() {
  const [charities, setCharities] = useState([]);
  const [donationStatus, setDonationStatus] = useState("");

  useEffect(() => {
    // Fetch charities from API (this could be a hardcoded list for now)
    const fetchCharities = async () => {
      // Example of charities data
      setCharities([
        { id: 1, name: "Operation Smile" },
        { id: 2, name: "Mary's Meals" },
        { id: 3, name: "Xingu Vivo" },
      ]);
    };
    
    fetchCharities();
  }, []);

  const handleDonation = async (amount, selectedCharities) => {
    const response = await submitDonation(amount, selectedCharities);
    if (response.success) {
      setDonationStatus("Donation successful! Thank you for your support!");
    } else {
      setDonationStatus("There was an issue with your donation.");
    }
  };

  return (
    <div>
      <h1>Welcome to Love That Gives Back</h1>
      <DonationForm charities={charities} handleDonation={handleDonation} />
      {donationStatus && <p>{donationStatus}</p>}
    </div>
  );
}

export default App;