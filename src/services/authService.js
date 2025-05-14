import api from './api';
import { jwtDecode } from 'jwt-decode';

const login = async (email, password) => {
  try {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    const response = await api.post('/token', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });

    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
      return true;
    }
    return false;
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
};

const logout = () => {
  localStorage.removeItem('token');
  window.location.href = '/login';
};

const isAuthenticated = () => {
  const token = localStorage.getItem('token');
  if (!token) return false;

  try {
    const decoded = jwtDecode(token);
    const currentTime = Date.now() / 1000;
    
    // Verificar se o token não expirou
    return decoded.exp > currentTime;
  } catch (error) {
    return false;
  }
};

const getCurrentUser = () => {
  try {
    const token = localStorage.getItem('token');
    if (!token) return null;
    
    const decoded = jwtDecode(token);
    return {
      id: decoded.sub,
      role: decoded.role,
    };
  } catch (error) {
    return null;
  }
};

const isAdmin = () => {
  const user = getCurrentUser();
  return user && user.role === 'admin';
};

const authService = {
  login,
  logout,
  isAuthenticated,
  getCurrentUser,
  isAdmin,
};

export default authService;
