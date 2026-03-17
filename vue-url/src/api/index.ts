import { useAuthStore } from "@/stores/auth"

export const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? ""

export async function apiFetch(path: string, options?: RequestInit): Promise<Response> {
  const response = await fetch(`${BASE_URL}${path}`, options)

  if (response.status === 401) {
    const auth = useAuthStore()
    if (auth.isAuthenticated) {
      auth.logout()
      window.location.href = "/login"
    }
  }

  return response
}