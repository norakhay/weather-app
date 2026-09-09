export type Weather = {
  city: string;
  country: string | null;
  temperature: number;
  condition: string;
  humidity: number;
  wind_speed: number;
  icon: string | null;
  icon_url: string | null;
};

export type SavedCity = {
  id: number;
  city_name: string;
  country: string | null;
  created_at: string | null;
};

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    ...options,
    headers: { "Content-Type": "application/json", ...(options?.headers || {}) },
  });
  const body = await response.json();
  if (!response.ok || !body.success) {
    throw new Error(body.error || "Request failed");
  }
  return body.data as T;
}

export function getWeather(city: string) {
  return request<Weather>(`/api/weather?city=${encodeURIComponent(city)}`);
}

export function listCities() {
  return request<SavedCity[]>("/api/cities");
}

export function saveCity(cityName: string) {
  return request<SavedCity>("/api/cities", {
    method: "POST",
    body: JSON.stringify({ city_name: cityName }),
  });
}

export function deleteCity(id: number) {
  return request<{ deleted: boolean }>(`/api/cities/${id}`, { method: "DELETE" });
}
