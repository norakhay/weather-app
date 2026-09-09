import { Weather } from "@/services/api";

type WeatherCardProps = {
  weather: Weather;
  onSave?: () => void;
  saving?: boolean;
};

export default function WeatherCard({ weather, onSave, saving }: WeatherCardProps) {
  return (
    <article className="card weather-card" data-testid="weather-card">
      <div className="weather-header">
        {weather.icon_url ? (
          <img src={weather.icon_url} alt={weather.condition} width={80} height={80} />
        ) : null}
        <div>
          <h2 data-testid="weather-city">
            {weather.city}
            {weather.country ? `, ${weather.country}` : ""}
          </h2>
          <p className="condition" data-testid="weather-condition">
            {weather.condition}
          </p>
        </div>
      </div>
      <p className="temperature" data-testid="weather-temperature">
        {Math.round(weather.temperature)}°C
      </p>
      <ul className="weather-details">
        <li>Humidity: {weather.humidity}%</li>
        <li>Wind: {weather.wind_speed} m/s</li>
      </ul>
      {onSave ? (
        <button type="button" data-testid="save-city" onClick={onSave} disabled={saving}>
          {saving ? "Saving..." : "Save city"}
        </button>
      ) : null}
    </article>
  );
}
