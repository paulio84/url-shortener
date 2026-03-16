export interface User {
  id: number
  email: string
  created_at: string
}

export interface ShortURL {
  id: number
  original_url: string
  short_code: string
  short_url: string
  clicks: number
  created_at: string
  user_id: number
}

export interface AuthResponse {
  access_token: string
  refresh_token: string
  user: User
}

export interface APIError {
  error: {
    status: number
    message: string
  }
}