import asyncio
import random
from pyppeteer import launch
from pyppeteer_stealth import stealth

users = [
    {'username': '13438186526', 'password': '19821124'},
    {'username': '15928968862', 'password': '19821124'}
]

async def login(username, password, browser):
    # Rest of the code...

async def main():
    browser = None  # Initialize browser variable with None
    try:
        browser = await launch(headless=False)
        await stealth(browser)

        tasks = []
        for user in users:
            username = user['username']
            password = user['password']
            task = asyncio.create_task(login(username, password, browser))
            tasks.append(task)

        await asyncio.gather(*tasks)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Close the browser if it's not None
        if browser is not None:
            await browser.close()
            await asyncio.sleep(3)  # Add a small delay
            await browser._cleanup()
            await browser._process.kill()

def delay_time():
    return random.uniform(1, 6)

if __name__ == "__main__":
    asyncio.run(main())
