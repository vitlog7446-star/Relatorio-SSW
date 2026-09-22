from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    page.goto("https://web.whatsapp.com/")

    print("Título da página:", page.title())

    browser.close()

print("Playwright funcionando!")
