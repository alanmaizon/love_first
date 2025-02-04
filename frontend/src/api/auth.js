const BASE_URL = "http://localhost:8000/api";

export const signup = async (email, password) => {
  const response = await fetch(`${BASE_URL}/register/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  return response.json();
};

export const login = async (email, password) => {
  const response = await fetch(`${BASE_URL}/login/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  return response.json();
};

export const logout = async (refreshToken) => {
  await fetch(`${BASE_URL}/logout/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh: refreshToken }),
  });
};
