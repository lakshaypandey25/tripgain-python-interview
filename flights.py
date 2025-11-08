from playwright.sync_api import sync_playwright
import json
from datetime import datetime, timedelta

future_date = (datetime.today() + timedelta(days=10)).strftime("%d-%m-%Y")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled"])
    context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.118 Safari/537.36")
    page = context.new_page()
    page.goto("https://www.budgetticket.in", timeout=60000)

    origin_selector = "input[placeholder='Select Origin City']"
    dest_selector = "input[placeholder='Select Destination City']"
    date_selector = "input[placeholder='Departure']"
    search_selector = "input[type='submit'][value='Search']"

    page.wait_for_selector(origin_selector, timeout=20000)
    page.evaluate(f"document.querySelector('{origin_selector}').value = 'Bangalore'; document.querySelector('{origin_selector}').dispatchEvent(new Event('input', {{bubbles: true}}));")

    page.wait_for_selector(dest_selector, timeout=20000)
    page.evaluate(f"document.querySelector('{dest_selector}').value = 'Delhi'; document.querySelector('{dest_selector}').dispatchEvent(new Event('input', {{bubbles: true}}));")

    page.wait_for_selector(date_selector, timeout=20000)
    page.evaluate(f"document.querySelector('{date_selector}').value = '{future_date}'; document.querySelector('{date_selector}').dispatchEvent(new Event('input', {{bubbles: true}}));")

    page.wait_for_selector(search_selector, timeout=20000)
    page.evaluate(f"document.querySelector('{search_selector}').click();")

    page.wait_for_selector(".searchResultList", timeout=60000)

    flights = page.query_selector_all(".searchResultList .flightRow")
    results = []
    for flight in flights:
        airline = flight.query_selector(".airlineName").inner_text().strip() if flight.query_selector(".airlineName") else ""
        number = flight.query_selector(".flightNumber").inner_text().strip() if flight.query_selector(".flightNumber") else ""
        dep_time = flight.query_selector(".depTime").inner_text().strip() if flight.query_selector(".depTime") else ""
        arr_time = flight.query_selector(".arrTime").inner_text().strip() if flight.query_selector(".arrTime") else ""
        price = flight.query_selector(".price").inner_text().strip() if flight.query_selector(".price") else ""
        results.append({
            "airline": airline,
            "flight_number": number,
            "departure_time": dep_time,
            "arrival_time": arr_time,
            "price": price
        })

    with open("flight_results.json", "w") as f:
        json.dump(results, f, indent=4)

    browser.close()
