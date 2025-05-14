import api from './api';

const getUsers = async () => {
  try {
    const response = await api.get('/users/');
    return response.data;
  } catch (error) {
    console.error('Error fetching users:', error);
    throw error;
  }
};

const getUser = async (id) => {
  try {
    const response = await api.get(`/users/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching user ${id}:`, error);
    throw error;
  }
};

const getCurrentUserInfo = async () => {
  try {
    const response = await api.get('/users/me');
    return response.data;
  } catch (error) {
    console.error('Error fetching current user info:', error);
    throw error;
  }
};

const createUser = async (userData) => {
  try {
    const response = await api.post('/users/', userData);
    return response.data;
  } catch (error) {
    console.error('Error creating user:', error);
    throw error;
  }
};

const updateUser = async (id, userData) => {
  try {
    const response = await api.put(`/users/${id}`, userData);
    return response.data;
  } catch (error) {
    console.error(`Error updating user ${id}:`, error);
    throw error;
  }
};

const deleteUser = async (id) => {
  try {
    await api.delete(`/users/${id}`);
    return true;
  } catch (error) {
    console.error(`Error deleting user ${id}:`, error);
    throw error;
  }
};

const userService = {
  getUsers,
  getUser,
  getCurrentUserInfo,
  createUser,
  updateUser,
  deleteUser,
};

export default userService;
