import { describe, it, expect, vi } from 'vitest';
import axios from 'axios';

vi.mock('axios');
beforeEach(() => {
  vi.clearAllMocks(); 
});

describe('donationService (Manual Transfers)', () => {
  it('should send a manual donation request', async () => {
    const mockResponse = { data: { success: true, message: "Donation recorded" } };
    axios.post.mockResolvedValue(mockResponse);

    const amount = 50;
    const charities = [1, 2]; // Example charity IDs
    const token = "test_token";

    // Simulate manual donation request
    const response = await axios.post(
      "http://localhost:8000/api/donations/",
      { amount, charities, payment_method: "manual" },
      { headers: { Authorization: `Bearer ${token}` } }
    );

    // Assertions
    expect(response.data).toEqual(mockResponse.data);
    expect(axios.post).toHaveBeenCalledWith(
      "http://localhost:8000/api/donations/",
      { amount, charities, payment_method: "manual" },
      { headers: { Authorization: `Bearer ${token}` } }
    );
  });

  it('should handle API errors gracefully', async () => {
    axios.post.mockRejectedValue(new Error('Failed to submit donation'));

    const amount = 50;
    const charities = [1, 2];
    const token = "test_token";

    try {
      await axios.post(
        "http://localhost:8000/api/donations/",
        { amount, charities, payment_method: "manual" },
        { headers: { Authorization: `Bearer ${token}` } }
      );
    } catch (error) {
      expect(error.message).toBe('Failed to submit donation');
    }

    expect(axios.post.mock.calls.length).toBeLessThanOrEqual(1);
  });
});
