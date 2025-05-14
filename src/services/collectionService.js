import api from './api';

const getCollections = async () => {
  try {
    const response = await api.get('/collections/');
    return response.data;
  } catch (error) {
    console.error('Error fetching collections:', error);
    throw error;
  }
};

const getCollection = async (id) => {
  try {
    const response = await api.get(`/collections/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching collection ${id}:`, error);
    throw error;
  }
};

const createCollection = async (collectionData) => {
  try {
    const response = await api.post('/collections/', collectionData);
    return response.data;
  } catch (error) {
    console.error('Error creating collection:', error);
    throw error;
  }
};

const assignCollection = async (collectionId, collectorId) => {
  try {
    const response = await api.post(`/collections/${collectionId}/assign`, {
      collector_id: collectorId,
    });
    return response.data;
  } catch (error) {
    console.error(`Error assigning collection ${collectionId}:`, error);
    throw error;
  }
};

const updateCollectionStatus = async (collectionId, status) => {
  try {
    const response = await api.post(`/collections/${collectionId}/status`, {
      status: status,
    });
    return response.data;
  } catch (error) {
    console.error(`Error updating collection ${collectionId} status:`, error);
    throw error;
  }
};

const collectionService = {
  getCollections,
  getCollection,
  createCollection,
  assignCollection,
  updateCollectionStatus,
};

export default collectionService;
