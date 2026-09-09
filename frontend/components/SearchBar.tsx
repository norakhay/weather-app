"use client";

import { FormEvent, useState } from "react";

type SearchBarProps = {
  onSearch: (city: string) => void;
  disabled?: boolean;
};

export default function SearchBar({ onSearch, disabled }: SearchBarProps) {
  const [city, setCity] = useState("");

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const trimmed = city.trim();
    if (!trimmed) return;
    onSearch(trimmed);
  }

  return (
    <form className="search-bar" onSubmit={handleSubmit}>
      <label htmlFor="city-search">City</label>
      <input
        id="city-search"
        data-testid="city-search"
        value={city}
        onChange={(event) => setCity(event.target.value)}
        placeholder="Search for a city"
        disabled={disabled}
      />
      <button type="submit" data-testid="search-button" disabled={disabled}>
        Search
      </button>
    </form>
  );
}
