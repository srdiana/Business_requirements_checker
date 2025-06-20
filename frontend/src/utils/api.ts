import axios, { AxiosError, AxiosInstance } from 'axios';
import { AnalysisResponse } from '../types';

const API_BASE_URL = 'http://localhost:8000/api';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    this.client.interceptors.request.use(
      (config) => {
        // Add any security headers here
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          // Handle unauthorized access
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  async analyzeDocuments(template: File, requirements: File): Promise<AnalysisResponse> {
    const formData = new FormData();
    formData.append('template', template);
    formData.append('requirements', requirements);

    try {
      const response = await this.client.post<AnalysisResponse>('/process', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(error.response?.data?.detail || 'Failed to analyze documents');
      }
      throw error;
    }
  }
}

export const api = new ApiClient(); 