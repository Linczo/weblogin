import asyncio
import random
from pyppeteer import launch
from pyppeteer_stealth import stealth
from pyppeteer.errors import NetworkError

users = [
    {'username': '13438186526', 'password': '19821124'},
    {'username': '15928968862', 'password': '19821124'}
]

async def login(username, password, browser):
    retry_count = 0
    success = False

    while retry_count < 3 and not success:
        try:
            page = await browser.newPage()
            await page.goto('http://wwww.cq17.com:12345/index/Index/Userlogins.html')

            # Wait for page to load
            await page.waitForSelector('#content_name')
            await page.waitForSelector('#content_password')
            await page.waitForSelector('.content_button button')

            # Enter username and password
            await page.type('#content_name', username)
            await page.type('#content_password', password)

            # Submit login form
            await page.click('.content_button button')

            try:
                # Wait for successful login and check if login was successful
                await page.waitForNavigation(timeout=5000)
                await page.waitForFunction('document.querySelector(".content_button button") === null')
            except NetworkError:
                # Timeout occurred or element not found, retry login
                retry_count += 1
                await page.close()
                continue

            print(f'Successful login for user: {username}')

            # Go to user center page
            await page.goto('http://wwww.cq17.com:12345/index/User/index.html')

            # Wait for page to load
            await page.waitForSelector('.signinqd')

            # Click on red envelope to claim
            await page.click('.signinqd')

            # Perform other operations after claiming the red envelope...

            print(f'Claimed red envelope for user: {username}')

            # Click on safe logout
            await page.click('.quit a')

            # Wait for logout to complete
            await page.waitForNavigation()

            print(f'Logged out for user: {username}')

            success = True
        except Exception as e:
            print(f"An error occurred during login for user {username}: {str(e)}")
            retry_count += 1

        await page.close()

    # Random delay
    await asyncio.sleep(delay_time())

async def main():
    browser = None  # Initialize browser variable with None
    try:
        browser = await launch(headless=True)  # Set headless=True for running in headless mode
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

def delay_time():
    return random.uniform(1, 6)

if __name__ == "__main__":
    asyncio.run(main())
