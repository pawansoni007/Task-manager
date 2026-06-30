// Thin fetch wrapper: resolves the base URL, sets JSON headers, and turns
// non-2xx responses into a typed ApiError so callers handle failures uniformly.

const BASE_URL = (
  import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'
).replace(/\/$/, '');

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

async function parseError(response: Response): Promise<string> {
  try {
    const body = await response.json();
    // FastAPI returns either a string detail or a validation error array.
    if (typeof body.detail === 'string') return body.detail;
    if (Array.isArray(body.detail) && body.detail[0]?.msg) {
      return body.detail[0].msg;
    }
  } catch {
    /* fall through to a generic message */
  }
  return `Request failed (${response.status})`;
}

export async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });

  if (!response.ok) {
    throw new ApiError(response.status, await parseError(response));
  }
  // 204 No Content has no body to parse.
  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}
