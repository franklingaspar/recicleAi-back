import React, { createContext, useState, useEffect, useContext } from 'react';
import authService from '../services/authService';
import userService from '../services/userService';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadUser = async () => {
      if (authService.isAuthenticated()) {
        try {
          const userData = await userService.getCurrentUserInfo();
          setUser(userData);
        } catch (error) {
          console.error('Error loading user:', error);
          authService.logout();
        }
      }
      setLoading(false);
    };

    loadUser();
  }, []);

  const login = async (email, password) => {
    try {
      const success = await authService.login(email, password);
      if (success) {
        const userData = await userService.getCurrentUserInfo();
        setUser(userData);
        return true;
      }
      return false;
    } catch (error) {
      console.error('Login error:', error);
      return false;
    }
  };

  const logout = () => {
    authService.logout();
    setUser(null);
  };

  const isAdmin = () => {
    return user && user.role === 'admin';
  };

  const isCollector = () => {
    return user && user.role === 'collector';
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        logout,
        isAuthenticated: !!user,
        isAdmin,
        isCollector,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);

export default AuthContext;
