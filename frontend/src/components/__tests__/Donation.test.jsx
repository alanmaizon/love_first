import { describe, it, expect, vi } from 'vitest';
import axios from 'axios';
import { createStripeCheckout, createPayPalPayment } from '../../services/donationService';

vi.mock('axios');

describe('donationService', () => {
  describe('createStripeCheckout', () => {
    it('should create a Stripe checkout session', async () => {
      const mockResponse = { data: { session_id: 'test_session_id', stripe_url: 'http://stripe.com' } };
      axios.post.mockResolvedValue(mockResponse);

      const amount = 100;
      const charities = ['charity1', 'charity2'];
      const token = 'test_token';

      const result = await createStripeCheckout(amount, charities, token);

      expect(result).toEqual(mockResponse.data);
      expect(axios.post).toHaveBeenCalledWith(
        'http://localhost:8000/api/stripe/checkout/',
        { amount, charities },
        { headers: { Authorization: `Bearer ${token}` } }
      );
    });
  });

  describe('createPayPalPayment', () => {
    it('should create a PayPal payment', async () => {
      const mockResponse = { data: { paypal_url: 'http://paypal.com' } };
      axios.post.mockResolvedValue(mockResponse);

      const amount = 100;
      const charities = ['charity1', 'charity2'];
      const token = 'test_token';

      const result = await createPayPalPayment(amount, charities, token);

      expect(result).toEqual(mockResponse.data);
      expect(axios.post).toHaveBeenCalledWith(
        'http://localhost:8000/api/paypal/payment/',
        { amount, charities },
        { headers: { Authorization: `Bearer ${token}` } }
      );
    });
  });
});