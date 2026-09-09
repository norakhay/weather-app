import { SavedCity } from "@/services/api";

type CityCardProps = {
  city: SavedCity;
  onDelete: (id: number) => void;
};

export default function CityCard({ city, onDelete }: CityCardProps) {
  return (
    <li className="city-card" data-testid="city-card">
      <span>
        {city.city_name}
        {city.country ? `, ${city.country}` : ""}
      </span>
      <button type="button" onClick={() => onDelete(city.id)} data-testid="delete-city">
        Remove
      </button>
    </li>
  );
}
