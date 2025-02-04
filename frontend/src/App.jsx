import React from "react";
import Signup from "./components/Signup";
import Login from "./components/Login";
import AuthProvider from "./context/AuthContext";

function App() {
  return (
    <AuthProvider>
      <div>
        <h1>Love That Gives Back</h1>
        <Signup />
        <Login />
      </div>
    </AuthProvider>
  );
}

export default App;
