import axios from "axios";

const API_URL = "http://localhost:8000/api"; // Update if needed

export const createStripeCheckout = async (amount, charities, token) => {
  try {
    const response = await axios.post(
      `${API_URL}/stripe/checkout/`,
      { amount, charities },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    return response.data; // { session_id, stripe_url }
  } catch (error) {
    console.error("Stripe Checkout Error:", error.response?.data || error);
    throw new Error(error.response?.data?.message || "Stripe payment failed");
  }
};

export const createPayPalPayment = async (amount, charities, token) => {
  try {
    const response = await axios.post(
      `${API_URL}/paypal/payment/`,
      { amount, charities },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    return response.data; // { paypal_url }
  } catch (error) {
    console.error("PayPal Payment Error:", error.response?.data || error);
    throw new Error(error.response?.data?.message || "PayPal payment failed");
  }
};