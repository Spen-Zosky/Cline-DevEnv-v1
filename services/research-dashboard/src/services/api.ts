import axios, { AxiosRequestConfig, AxiosResponse } from 'axios';

// Create axios instance with default config
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  timeout: parseInt(process.env.REACT_APP_API_TIMEOUT || '30000'),
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for handling errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle specific error cases
    if (error.response) {
      // Server responded with a status code outside of 2xx
      if (error.response.status === 401) {
        // Unauthorized - clear token and redirect to login
        localStorage.removeItem('auth_token');
        // Redirect to login page if needed
      }
    }
    return Promise.reject(error);
  }
);

// API service methods
const apiService = {
  // Health checks
  getApiHealth: (): Promise<AxiosResponse> => api.get('/health'),
  getServicesHealth: (): Promise<AxiosResponse> => api.get('/health/services'),
  
  // Services
  getServices: (): Promise<AxiosResponse> => api.get('/api/services'),
  getServiceCategories: (): Promise<AxiosResponse> => api.get('/api/services/categories'),
  getServiceById: (id: string): Promise<AxiosResponse> => api.get(`/api/services/${id}`),
  getServiceStatus: (id: string): Promise<AxiosResponse> => api.get(`/api/services/${id}/status`),
  restartService: (id: string): Promise<AxiosResponse> => api.post(`/api/services/${id}/restart`),
  startService: (id: string): Promise<AxiosResponse> => api.post(`/api/services/${id}/start`),
  stopService: (id: string): Promise<AxiosResponse> => api.post(`/api/services/${id}/stop`),
  
  // System
  getSystemInfo: (): Promise<AxiosResponse> => api.get('/api/system/info'),
  getSystemMetrics: (): Promise<AxiosResponse> => api.get('/api/system/metrics'),
  getSystemLogs: (params?: { service?: string; level?: string; limit?: number }): Promise<AxiosResponse> => 
    api.get('/api/system/logs', { params }),
  deploySystem: (data: { services?: string[]; environment?: string }): Promise<AxiosResponse> => 
    api.post('/api/system/deploy', data),
  
  // Data Collection
  getCrawlJobs: (): Promise<AxiosResponse> => api.get('/api/crawler/jobs'),
  createCrawlJob: (data: any): Promise<AxiosResponse> => api.post('/api/crawler/jobs', data),
  getScrapeJobs: (): Promise<AxiosResponse> => api.get('/api/scraper/jobs'),
  createScrapeJob: (data: any): Promise<AxiosResponse> => api.post('/api/scraper/jobs', data),
  
  // Data Processing
  getPreprocessingJobs: (): Promise<AxiosResponse> => api.get('/api/preprocessor/jobs'),
  createPreprocessingJob: (data: any): Promise<AxiosResponse> => api.post('/api/preprocessor/jobs', data),
  getTransformationJobs: (): Promise<AxiosResponse> => api.get('/api/transformer/jobs'),
  createTransformationJob: (data: any): Promise<AxiosResponse> => api.post('/api/transformer/jobs', data),
  
  // ML Framework
  getTrainingJobs: (): Promise<AxiosResponse> => api.get('/api/ml-trainer/jobs'),
  createTrainingJob: (data: any): Promise<AxiosResponse> => api.post('/api/ml-trainer/jobs', data),
  getEvaluationJobs: (): Promise<AxiosResponse> => api.get('/api/ml-evaluator/jobs'),
  createEvaluationJob: (data: any): Promise<AxiosResponse> => api.post('/api/ml-evaluator/jobs', data),
  
  // Web Generator
  getGenerationJobs: (): Promise<AxiosResponse> => api.get('/api/web-generator/jobs'),
  createGenerationJob: (data: any): Promise<AxiosResponse> => api.post('/api/web-generator/jobs', data),
  
  // Generic request method for custom endpoints
  request: <T = any>(config: AxiosRequestConfig): Promise<AxiosResponse<T>> => api(config),
};

export default apiService;
