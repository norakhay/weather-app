import os

from playwright.sync_api import expect

BASE_URL = os.getenv("BASE_URL", "http://localhost:3000")


def test_user_can_search_for_a_city(page):
    page.goto(BASE_URL)
    page.get_by_test_id("city-search").fill("Amman")
    page.get_by_test_id("search-button").click()

    expect(page.get_by_test_id("weather-card")).to_be_visible()
    expect(page.get_by_test_id("weather-city")).to_contain_text("Amman")
    expect(page.get_by_test_id("weather-temperature")).to_contain_text("°C")


def test_user_can_save_a_city(page):
    page.goto(BASE_URL)
    page.get_by_test_id("city-search").fill("London")
    page.get_by_test_id("search-button").click()
    expect(page.get_by_test_id("weather-card")).to_be_visible()

    page.get_by_test_id("save-city").click()
    expect(page.get_by_test_id("saved-cities")).to_contain_text("London")


def test_user_can_delete_a_saved_city(page):
    page.goto(BASE_URL)
    page.get_by_test_id("city-search").fill("Amman")
    page.get_by_test_id("search-button").click()
    expect(page.get_by_test_id("weather-card")).to_be_visible()
    page.get_by_test_id("save-city").click()

    amman_card = page.get_by_test_id("city-card").filter(has_text="Amman")
    expect(amman_card).to_be_visible()
    amman_card.get_by_test_id("delete-city").click()
    expect(page.get_by_test_id("saved-cities")).not_to_contain_text("Amman")


def test_invalid_city_shows_an_error(page):
    page.goto(BASE_URL)
    page.get_by_test_id("city-search").fill("Atlantis")
    page.get_by_test_id("search-button").click()

    expect(page.get_by_test_id("error-message")).to_have_text("City not found")
    expect(page.get_by_test_id("weather-card")).to_have_count(0)
