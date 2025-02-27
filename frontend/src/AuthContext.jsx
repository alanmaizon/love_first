import { createContext, useState, useEffect, useContext } from 'react';

const LOCAL_STORAGE_NAMESPACE = 'appAuthentication';

const authStorage = {
  set: (key, value) => {
    sessionStorage.setItem(`${LOCAL_STORAGE_NAMESPACE}.${key}`, JSON.stringify(value));
  },
  get: (key) => {
    const item = sessionStorage.getItem(`${LOCAL_STORAGE_NAMESPACE}.${key}`);
    return item ? JSON.parse(item) : null;
  },
  remove: (key) => {
    sessionStorage.removeItem(`${LOCAL_STORAGE_NAMESPACE}.${key}`);
  },
  clear: () => {
    Object.keys(sessionStorage)
      .filter(key => key.startsWith(`${LOCAL_STORAGE_NAMESPACE}.`))
      .forEach(key => sessionStorage.removeItem(key));
  }
};

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(() => !!authStorage.get('access_token'));
  const [username, setUsername] = useState(() => authStorage.get('username') || null);
  const [token, setToken] = useState(() => authStorage.get('access_token') || null);

  useEffect(() => {
    checkLoginStatus();
  }, []);

  const checkLoginStatus = () => {
    const token = authStorage.get('access_token');
    const storedUsername = authStorage.get('username');

    if (token && storedUsername) {
      setIsLoggedIn(true);
      setUsername(storedUsername);
      setToken(token);
    } else {
      setIsLoggedIn(false);
      setUsername(null);
      setToken(null);
    }
  };

  const login = (accessToken, refreshToken, user) => {
    authStorage.set('access_token', accessToken);
    authStorage.set('refresh_token', refreshToken);
    authStorage.set('username', user);
    setIsLoggedIn(true);
    setUsername(user);
    setToken(accessToken);
  };

  const logout = () => {
    authStorage.clear();
    setIsLoggedIn(false);
    setUsername(null);
    setToken(null);
  };

  const getAccessToken = () => authStorage.get('access_token');
  const getRefreshToken = () => authStorage.get('refresh_token');

  return (
    <AuthContext.Provider value={{
      isLoggedIn,
      username,
      token,
      login,
      logout,
      checkLoginStatus,
      getAccessToken,
      getRefreshToken
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);