import { useEffect } from 'react'
import { BrowserRouter as Router, Route, Routes, NavLink, useNavigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './AuthContext'
import { Register, Login } from './components/Authentication'
import ProtectedRoute from "./components/ProtectedRoute"; 
import DonationForm from "./components/DonationForm";
import DonationHistory from "./components/DonationHistory";
import Success from './components/Success';

import './App.css'

const Home = () => {
  const { isLoggedIn, username} = useAuth()
  return (
    <h2>
      {isLoggedIn
        ? `Welcome, ${username}! You're logged in.`
        : "Hi, please log in (or register) to use the site"}
    </h2>
  )
}

const PrivateComponent = () => {
  const { isLoggedIn, username } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(false);
    if (!isLoggedIn) {
      navigate("/login");
    }
  }, [isLoggedIn, navigate]);

  if (loading) return <p>Loading...</p>;
  return isLoggedIn ? <h2>Welcome {username}! This is the private section.</h2> : null;
};


const Navigation = () => {
  const { isLoggedIn, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    console.log('Logout successful')
    navigate('/')
  }

  return (
    <nav>
      <h1><NavLink to="/">Love That Gives Back 💕</NavLink></h1>
      <ul>
        {isLoggedIn ? (
          <>
            <li><NavLink to="/private">Private</NavLink></li>
            <li><NavLink to="/donate">Donate</NavLink></li>
            <li><NavLink to="/history">History</NavLink></li>
            <li><button onClick={handleLogout}>Logout</button></li>
          </>
        ) : (
          <>
            <li><NavLink to="/register">Register</NavLink></li>
            <li><NavLink to="/login">Login</NavLink></li>
          </>
        )}
      </ul>
    </nav>
  )
}

const AppContent = () => (
  <div className="App">
    <Navigation />

    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/register" element={<Register />} />
      
      <Route path="/login" element={<Login />} />

      {/* Protected routes */}
      <Route
        path="/private"
        element={
          <ProtectedRoute>
            <PrivateComponent />
          </ProtectedRoute>
        }
      />
      
      {/* You can protect other routes too! */}
      <Route
        path="/donate"
        element={
          <ProtectedRoute>
            <DonationForm />
          </ProtectedRoute>
        }
      />
      <Route
        path="/history"
        element={
          <ProtectedRoute>
            <DonationHistory />
          </ProtectedRoute>
        }
      />

      {/* Add the success route */}
      <Route path="/success" element={<Success />} />
      
      <Route path="*" element={<h2>404 Not Found</h2>} />
    </Routes>
  </div>
)

const App = () => {
  return (
    <AuthProvider>
      <Router>
        <AppContent />
      </Router>
    </AuthProvider>
  )
}

export default App
