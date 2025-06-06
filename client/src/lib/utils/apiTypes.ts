/**
 * API response and error types
 */

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  status: number;
  timestamp: string;
}

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public code?: string,
    public details?: any,
  ) {
    super(message);
    this.name = "ApiError";
  }
}
