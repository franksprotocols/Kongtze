/**
 * API client configuration and utilities for Kongtze frontend
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export interface APIError {
  detail: string;
  status?: number;
}

class APIClient {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  private getHeaders(token?: string): HeadersInit {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    return headers;
  }

  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      const error: APIError = await response.json().catch(() => ({
        detail: 'An unexpected error occurred',
        status: response.status,
      }));
      throw error;
    }

    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      return response.json();
    }

    return {} as T;
  }

  async get<T>(endpoint: string, token?: string): Promise<T> {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'GET',
      headers: this.getHeaders(token),
    });

    return this.handleResponse<T>(response);
  }

  async post<T>(endpoint: string, data?: any, token?: string): Promise<T> {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'POST',
      headers: this.getHeaders(token),
      body: JSON.stringify(data),
    });

    return this.handleResponse<T>(response);
  }

  async put<T>(endpoint: string, data: any, token?: string): Promise<T> {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'PUT',
      headers: this.getHeaders(token),
      body: JSON.stringify(data),
    });

    return this.handleResponse<T>(response);
  }

  async delete<T>(endpoint: string, token?: string): Promise<T> {
    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'DELETE',
      headers: this.getHeaders(token),
    });

    return this.handleResponse<T>(response);
  }

  async upload<T>(endpoint: string, formData: FormData, token?: string): Promise<T> {
    const headers: HeadersInit = {};

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'POST',
      headers,
      body: formData,
    });

    return this.handleResponse<T>(response);
  }
}

export const apiClient = new APIClient();
