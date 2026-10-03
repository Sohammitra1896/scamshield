import axios from 'axios';

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const fetchHealth = async () => {
  const response = await api.get('/health');
  return response.data;
};

export const analyzeMessage = async (message) => {
  const response = await api.post(
    '/analyze/message',
    {
      message,
    },
  );

  return response.data;
};

export const analyzeURL = async (url) => {
  const response = await api.post(
    '/analyze/url',
    {
      url,
    },
  );

  return response.data;
};

export const analyzeScreenshot = async (file) => {
  const formData = new FormData();

  formData.append('file', file);

  const response = await api.post(
    '/analyze/screenshot',
    formData,
    {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    },
  );

  return response.data;
};

export const fetchHistory = async ({
  search = '',
  riskLevel = '',
  skip = 0,
  limit = 20,
} = {}) => {
  const response = await api.get(
    '/history',
    {
      params: {
        search: search || undefined,
        risk_level: riskLevel || undefined,
        skip,
        limit,
      },
    },
  );

  return response.data;
};

export const fetchHistoryRecord = async (scanId) => {
  const response = await api.get(
    `/history/${scanId}`,
  );

  return response.data;
};

export const fetchStats = async () => {
  const response = await api.get('/stats');
  return response.data;
};

export default api;
