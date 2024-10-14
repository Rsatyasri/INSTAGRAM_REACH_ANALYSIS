import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to initialize WebDriver
def setup_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver

# Function to log in to Instagram
def instagram_login(driver, username, password):
    driver.get("https://www.instagram.com")
    time.sleep(5)

    username_input = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')
    username_input.send_keys(username)

    password_input = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')
    password_input.send_keys(password)

    login_button = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')
    login_button.click()
    time.sleep(5)
    user_ids = set()
    hashtags = ['food', 'foodblogger', 'foodphotography']
    for hashtag in hashtags:
        driver.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
        time.sleep(5)  # Wait for the page to load

        # Scroll to load posts
        for _ in range(3):  # Adjust range for more scrolling
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)

        # Find posts and collect user IDs
        posts = driver.find_elements(By.XPATH, '//a[contains(@href, "/p/")]')
        for post in posts[:150]:  # Limit to first 150 posts
            post_url = post.get_attribute('href')
            user_id = post_url.split("/")[-2]  # Extract user ID from the URL
            user_ids.add(user_id)
    user_ids=list(user_ids)
    print(f"Total unique user IDs scraped: {len(user_ids)}")
    save_to_csv(user_ids, 'instagram_user_ids.csv')

# Function to save user IDs to a CSV file
def save_to_csv(user_ids, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["UserID"])  # Header
        for user_id in user_ids:
            writer.writerow([user_id])

    # Function to scrape user IDs from hashtags



def main():
    driver = setup_driver()
    instagram_login(driver, 'peaceful_soul04_', 'shashi@2004')

    driver.quit()

if __name__ == "__main__":
    main()
