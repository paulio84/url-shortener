import { apiFetch, BASE_URL } from ".";

export function fullShortUrl(shortUrl: string): string {
  return `${BASE_URL}${shortUrl}`
}

export async function fetchURLs(accessToken: string): Promise<Response> {
  return apiFetch("/api/urls", {
    headers: { Authorization: `Bearer ${accessToken}` },
  })
}

export async function shortenURL(originalUrl: string, accessToken: string): Promise<Response> {
  return apiFetch("/api/shorten", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`,
    },
    body: JSON.stringify({ url: originalUrl }),
  })
}