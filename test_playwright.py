import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        page.on('console', lambda msg: print(f'CONSOLE {msg.type}: {msg.text}'))
        page.on('pageerror', lambda exc: print(f'PAGE ERROR: {exc}'))
        
        try:
            print('Navigating...')
            response = await page.goto('http://localhost:5174', timeout=10000)
            print(f'HTTP Status Code: {response.status if response else "None"}')
            await asyncio.sleep(2)
        except Exception as e:
            print(f'Error: {e}')
        finally:
            await browser.close()

asyncio.run(run())
