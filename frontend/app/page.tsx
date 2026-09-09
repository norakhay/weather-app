"use client";

import { useEffect, useState } from "react";

import ErrorMessage from "@/components/ErrorMessage";
import LoadingState from "@/components/LoadingState";
import SavedCities from "@/components/SavedCities";
import SearchBar from "@/components/SearchBar";
import WeatherCard from "@/components/WeatherCard";
import { deleteCity, getWeather, listCities, saveCity, SavedCity, Weather } from "@/services/api";

export default function HomePage() {
  const [weather, setWeather] = useState<Weather | null>(null);
  const [weatherLoading, setWeatherLoading] = useState(false);
  const [weatherError, setWeatherError] = useState<string | null>(null);
  const [cities, setCities] = useState<SavedCity[]>([]);
  const [citiesLoading, setCitiesLoading] = useState(true);
  const [citiesError, setCitiesError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    listCities()
      .then(setCities)
      .catch((err: Error) => setCitiesError(err.message))
      .finally(() => setCitiesLoading(false));
  }, []);

  async function search(city: string) {
    setWeatherLoading(true);
    setWeatherError(null);
    try {
      setWeather(await getWeather(city));
    } catch (err) {
      setWeather(null);
      setWeatherError(err instanceof Error ? err.message : "Could not load weather");
    } finally {
      setWeatherLoading(false);
    }
  }

  async function handleSave() {
    if (!weather) return;
    setSaving(true);
    setCitiesError(null);
    try {
      await saveCity(weather.city);
      setCities(await listCities());
    } catch (err) {
      setCitiesError(err instanceof Error ? err.message : "Could not save city");
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete(id: number) {
    setCitiesError(null);
    try {
      await deleteCity(id);
      setCities((current) => current.filter((city) => city.id !== id));
    } catch (err) {
      setCitiesError(err instanceof Error ? err.message : "Could not delete city");
    }
  }

  return (
    <main className="page">
      <h1>Weather App</h1>
      <p className="subtitle">Search a city, view current weather, and save favorites.</p>
      <div className="layout">
        <section className="card">
          <SearchBar onSearch={search} disabled={weatherLoading} />
          {weatherLoading ? <LoadingState label="Fetching weather..." /> : null}
          {weatherError ? <ErrorMessage message={weatherError} /> : null}
          {weather && !weatherLoading ? (
            <WeatherCard weather={weather} onSave={handleSave} saving={saving} />
          ) : null}
        </section>
        <div>
          {citiesError ? <ErrorMessage message={citiesError} /> : null}
          <SavedCities cities={cities} loading={citiesLoading} onDelete={handleDelete} />
        </div>
      </div>
    </main>
  );
}
