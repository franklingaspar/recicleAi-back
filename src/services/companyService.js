import api from './api';

const getCompanies = async () => {
  try {
    const response = await api.get('/companies/');
    return response.data;
  } catch (error) {
    console.error('Error fetching companies:', error);
    throw error;
  }
};

const getCompany = async (id) => {
  try {
    const response = await api.get(`/companies/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching company ${id}:`, error);
    throw error;
  }
};

const createCompany = async (companyData) => {
  try {
    const response = await api.post('/companies/', companyData);
    return response.data;
  } catch (error) {
    console.error('Error creating company:', error);
    throw error;
  }
};

const updateCompany = async (id, companyData) => {
  try {
    const response = await api.put(`/companies/${id}`, companyData);
    return response.data;
  } catch (error) {
    console.error(`Error updating company ${id}:`, error);
    throw error;
  }
};

const deleteCompany = async (id) => {
  try {
    await api.delete(`/companies/${id}`);
    return true;
  } catch (error) {
    console.error(`Error deleting company ${id}:`, error);
    throw error;
  }
};

const companyService = {
  getCompanies,
  getCompany,
  createCompany,
  updateCompany,
  deleteCompany,
};

export default companyService;
