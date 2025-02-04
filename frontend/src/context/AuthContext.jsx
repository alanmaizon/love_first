import React, { createContext, useState } from "react";
import { logout } from "../api/auth";

export const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(localStorage.getItem("access") ? true : false);

  const handleLogout = async () => {
    const refreshToken = localStorage.getItem("refresh");
    if (refreshToken) {
      await logout(refreshToken);
    }
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    setUser(false);
  };

  return (
    <AuthContext.Provider value={{ user, setUser, handleLogout }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
