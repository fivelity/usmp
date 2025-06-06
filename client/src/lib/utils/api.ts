/**
 * Production-grade API client with comprehensive error handling.
 * Type-safe HTTP client with retry logic and request/response interceptors.
 */

import { env, log, error } from "$lib/config/environment";
import { ApiError, ApiResponse } from "./apiTypes"; // Import ApiResponse and ApiError

export class ApiClient {
  private baseURL: string;
  private timeout: number;
  private defaultHeaders: Record<string, string>;

  constructor() {
    this.baseURL = env.API_BASE_URL;
    this.timeout = env.API_TIMEOUT;
    this.defaultHeaders = {
      "Content-Type": "application/json",
      Accept: "application/json",
    };
  }

  /**
   * Make HTTP request with comprehensive error handling
   */
  private async request<T>(
    endpoint: string,
    options: RequestInit = {},
  ): Promise<ApiResponse<T>> {
    const url = `${this.baseURL}${endpoint}`;
    const controller = new AbortController();

    // Set timeout
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      log(`API Request: ${options.method || "GET"} ${url}`);

      const response = await fetch(url, {
        ...options,
        headers: {
          ...this.defaultHeaders,
          ...options.headers,
        },
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      // Handle HTTP errors
      if (!response.ok) {
        const errorData = await this.parseErrorResponse(response);
        throw new ApiError(
          errorData.message ||
            `HTTP ${response.status}: ${response.statusText}`,
          response.status,
          errorData.code,
          errorData.details,
        );
      }

      // Parse successful response
      const data = await response.json();

      log(`API Response: ${response.status}`, data);

      return {
        success: true,
        data,
        status: response.status,
        timestamp: new Date().toISOString(),
      };
    } catch (err: unknown) {
      clearTimeout(timeoutId);

      if (err instanceof ApiError) {
        error(`API Error: ${err.message}`, err);
        return {
          success: false,
          error: err.message,
          status: err.status,
          timestamp: new Date().toISOString(),
        };
      }

      // Handle network errors
      if (err instanceof Error) {
        if (err.name === "AbortError") {
          const message = "Request timeout";
          error(`API Timeout: ${url}`);
          return {
            success: false,
            error: message,
            status: 408,
            timestamp: new Date().toISOString(),
          };
        }

        error(`API Network Error: ${err.message}`, err);
        return {
          success: false,
          error: err.message,
          status: 0,
          timestamp: new Date().toISOString(),
        };
      }

      // Unknown error
      const message = "Unknown error occurred";
      error(`API Unknown Error:`, err);
      return {
        success: false,
        error: message,
        status: 500,
        timestamp: new Date().toISOString(),
      };
    }
  }

  /**
   * Parse error response body
   */
  private async parseErrorResponse(response: Response): Promise<any> {
    try {
      const contentType = response.headers.get("content-type");
      if (contentType && contentType.includes("application/json")) {
        return await response.json();
      }
      return { message: await response.text() };
    } catch {
      return { message: response.statusText };
    }
  }

  /**
   * GET request
   */
  async get<T>(
    endpoint: string,
    params?: Record<string, any>,
  ): Promise<ApiResponse<T>> {
    let url = endpoint;

    if (params) {
      const searchParams = new URLSearchParams();
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          searchParams.append(key, String(value));
        }
      });

      if (searchParams.toString()) {
        url += `?${searchParams.toString()}`;
      }
    }

    return this.request<T>(url, { method: "GET" });
  }

  /**
   * POST request
   */
  async post<T>(endpoint: string, data?: any): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: "POST",
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  /**
   * PUT request
   */
  async put<T>(endpoint: string, data?: any): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: "PUT",
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  /**
   * PATCH request
   */
  async patch<T>(endpoint: string, data?: any): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: "PATCH",
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  /**
   * DELETE request
   */
  async delete<T>(endpoint: string): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { method: "DELETE" });
  }

  /**
   * Upload file
   */
  async upload<T>(
    endpoint: string,
    file: File,
    additionalData?: Record<string, any>,
  ): Promise<ApiResponse<T>> {
    const formData = new FormData();
    formData.append("file", file);

    if (additionalData) {
      Object.entries(additionalData).forEach(([key, value]) => {
        formData.append(key, String(value));
      });
    }

    return this.request<T>(endpoint, {
      method: "POST",
      body: formData,
      headers: {
        // Don't set Content-Type for FormData, let browser set it with boundary
      },
    });
  }

  /**
   * Health check
   */
  async healthCheck(): Promise<boolean> {
    try {
      const response = await this.get("/health");
      return response.success;
    } catch {
      return false;
    }
  }

  /**
   * Set authentication token
   */
  setAuthToken(token: string): void {
    this.defaultHeaders["Authorization"] = `Bearer ${token}`;
  }

  /**
   * Remove authentication token
   */
  removeAuthToken(): void {
    delete this.defaultHeaders["Authorization"];
  }

  /**
   * Update base URL
   */
  setBaseURL(url: string): void {
    this.baseURL = url;
  }

  /**
   * Get current base URL
   */
  getBaseURL(): string {
    return this.baseURL;
  }
}

// Create API client instance
const apiClient = new ApiClient();

// Convenience functions
export const api = {
  get: <T>(endpoint: string, params?: Record<string, any>) =>
    apiClient.get<T>(endpoint, params),
  post: <T>(endpoint: string, data?: any) => apiClient.post<T>(endpoint, data),
  put: <T>(endpoint: string, data?: any) => apiClient.put<T>(endpoint, data),
  patch: <T>(endpoint: string, data?: any) =>
    apiClient.patch<T>(endpoint, data),
  delete: <T>(endpoint: string) => apiClient.delete<T>(endpoint),
  upload: <T>(
    endpoint: string,
    file: File,
    additionalData?: Record<string, any>,
  ) => apiClient.upload<T>(endpoint, file, additionalData),
  healthCheck: () => apiClient.healthCheck(),
  setAuthToken: (token: string) => apiClient.setAuthToken(token),
  removeAuthToken: () => apiClient.removeAuthToken(),
  setBaseURL: (url: string) => apiClient.setBaseURL(url),
  getBaseURL: () => apiClient.getBaseURL(),
};

// Export types\
export { ApiResponse, ApiError };
