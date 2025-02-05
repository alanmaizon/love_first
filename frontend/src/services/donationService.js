import axios from "axios";

const API_URL = "http://localhost:8000/api"; // Update if needed

export const createStripeCheckout = async (amount, charities, token) => {
  const response = await axios.post(
    `${API_URL}/stripe/checkout/`,
    { amount, charities },
    { headers: { Authorization: `Bearer ${token}` } }
  );
  return response.data; // { session_id, stripe_url }
};

export const createPayPalPayment = async (amount, charities, token) => {
  const response = await axios.post(
    `${API_URL}/paypal/payment/`,
    { amount, charities },
    { headers: { Authorization: `Bearer ${token}` } }
  );
  return response.data; // { paypal_url }
};
