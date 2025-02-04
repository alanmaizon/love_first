const BASE_URL = "http://localhost:8000/api";

export const submitDonation = async (amount, selectedCharities) => {
  const accessToken = localStorage.getItem("access");

  const response = await fetch(`${BASE_URL}/donations/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`,
    },
    body: JSON.stringify({
      amount,
      charities: selectedCharities,
    }),
  });
  
  return response.json();
};
