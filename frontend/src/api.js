const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:5000/api/v1";

// Keep access tokens in application memory; do not persist bearer tokens in localStorage.
let accessToken = null;

export function setAccessToken(token) {
  accessToken = token;
}

export async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
      ...options.headers,
    },
  });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(payload?.error?.message || "The request could not be completed.");
  }
  return payload;
}
