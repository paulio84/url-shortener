import { BASE_URL } from ".";

export function fullShortUrl(shortUrl: string): string {
  return `${BASE_URL}${shortUrl}`
}

export async function fetchURLs(accessToken: string): Promise<Response> {
  return fetch(`${BASE_URL}/api/urls`, {
    headers: { Authorization: `Bearer ${accessToken}` },
  })
}

export async function shortenURL(originalUrl: string, accessToken: string): Promise<Response> {
  return fetch(`${BASE_URL}/api/shorten`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`,
    },
    body: JSON.stringify({ url: originalUrl }),
  })
}