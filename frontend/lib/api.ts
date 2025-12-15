/**
 * API Client for Clarity LMS Backend
 *
 * Configured axios instance with:
 * - Base URL from environment variable
 * - Dev Auth header injection (x-user-email)
 * - Request/response interceptors
 */

import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

/**
 * Axios instance configured for Clarity LMS API
 */
export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 second timeout
});

/**
 * Request interceptor: Inject Dev Auth header
 *
 * The backend uses a "Dev Auth" system where the user is identified
 * by the x-user-email header. In production, this would be replaced
 * with proper JWT authentication.
 *
 * Priority:
 * 1. Check localStorage for 'x-user-email'
 * 2. Default to 'student@clarity.com' for easy testing
 */
api.interceptors.request.use(
  (config) => {
    // Get user email from localStorage (browser only)
    let userEmail = 'student@clarity.com'; // Default

    if (typeof window !== 'undefined') {
      const storedEmail = localStorage.getItem('x-user-email');
      if (storedEmail) {
        userEmail = storedEmail;
      }
    }

    // Inject dev auth header
    config.headers['x-user-email'] = userEmail;

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

/**
 * Response interceptor: Handle errors globally
 */
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Log errors for debugging
    if (error.response) {
      // Server responded with error status
      console.error('API Error:', {
        status: error.response.status,
        data: error.response.data,
        url: error.config?.url,
      });
    } else if (error.request) {
      // Request made but no response
      console.error('Network Error:', {
        message: 'No response from server',
        url: error.config?.url,
      });
    } else {
      // Error setting up request
      console.error('Request Error:', error.message);
    }

    return Promise.reject(error);
  }
);

/**
 * Helper function to set the current user email
 * This is used for testing different user roles
 */
export const setUserEmail = (email: string) => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('x-user-email', email);
  }
};

/**
 * Helper function to get the current user email
 */
export const getUserEmail = (): string => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('x-user-email') || 'student@clarity.com';
  }
  return 'student@clarity.com';
};

/**
 * Helper function to clear user auth
 */
export const clearUserEmail = () => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('x-user-email');
  }
};
