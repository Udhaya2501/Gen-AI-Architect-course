from playwright.sync_api import sync_playwright
import csv

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    # Open website
    page.goto("https://quotes.toscrape.com")
    
    # Get all quote elements
    quotes = page.locator(".quote")
    
    # Open CSV file
    with open("quotes.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        # Write header
        writer.writerow(["Quote", "Author"])
        
        # Loop through quotes
        for i in range(quotes.count()):
            quote_text = quotes.nth(i).locator(".text").inner_text()
            author = quotes.nth(i).locator(".author").inner_text()
            
            writer.writerow([quote_text, author])
    
    browser.close()

print("Data saved to quotes.csv")