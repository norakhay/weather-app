import { SavedCity } from "@/services/api";

import CityCard from "@/components/CityCard";
import LoadingState from "@/components/LoadingState";

type SavedCitiesProps = {
  cities: SavedCity[];
  loading: boolean;
  onDelete: (id: number) => void;
};

export default function SavedCities({ cities, loading, onDelete }: SavedCitiesProps) {
  return (
    <section className="card" data-testid="saved-cities">
      <h2>Saved cities</h2>
      {loading ? <LoadingState label="Loading saved cities..." /> : null}
      {!loading && cities.length === 0 ? (
        <p className="muted">No saved cities yet.</p>
      ) : null}
      <ul className="city-list">
        {cities.map((city) => (
          <CityCard key={city.id} city={city} onDelete={onDelete} />
        ))}
      </ul>
    </section>
  );
}
