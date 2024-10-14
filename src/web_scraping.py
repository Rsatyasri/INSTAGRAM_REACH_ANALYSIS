import json
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import re

# Function to remove emojis and non-ASCII characters from the bio
def clean_bio(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII characters (including emojis)

# Function to scrape post URLs from the user's profile
def scrape_profile_posts(driver, username):
    driver.get("https://www.instagram.com/" + username + "/")
    time.sleep(3)

    post_urls = set()  # Use a set to prevent duplicates
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Wait for the page to load

        try:
            # Get all post links
            post_links = driver.find_elements(By.XPATH, '//a[contains(@href, "/p/")]')
            for link in post_links:
                post_urls.add(link.get_attribute('href'))  # Add URLs to the set to avoid duplicates
        except:
            pass  # Ignore errors and continue

        # Break if no new posts are loaded
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    return list(post_urls)

# Function to scrape comments for a given post
def scrape_comments(driver, post_url):
    driver.get(post_url)
    time.sleep(2)

    comments_data = []
    for _ in range(3):  # Adjust this range to load more comments
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    try:
        comments = driver.find_elements(By.CSS_SELECTOR, 'div._a9zr')

        for comment in comments:
            try:
                username = comment.find_element(By.CSS_SELECTOR, 'h3._a9zc a').text
                text = comment.find_element(By.CSS_SELECTOR, 'div._a9zs > span._ap3a').text
                comments_data.append({'username': username, 'comment': text})
            except:
                pass  # Ignore errors and continue
    except:
        pass  # Ignore errors and continue

    return comments_data

# Function to scrape likes, hashtags, location, date, and comments from a post
def scrape_post_details(driver, post_url):
    driver.get(post_url)
    time.sleep(3)  # Wait for the post page to load

    details = {}

    # Scrape likes
    try:
        likes_element = driver.find_element(By.XPATH, '//span[contains(@class, "xdj266r")]/ancestor::span[contains(@class, "x193iq5w")]/span')
        likes = likes_element.text.split(' ')[0]  # Extract only the number of likes
        details['likes'] = likes
    except:
        details['likes'] = "Not Available"

    # Scrape hashtags
    try:
        hashtag_elements = driver.find_elements(By.XPATH, '//a[contains(@href, "/explore/tags/")]')
        hashtags_list = [hashtag.text for hashtag in hashtag_elements]
        details['hashtags'] = hashtags_list
    except:
        details['hashtags'] = "Not Available"

    # Scrape location (if available)
    try:
        location_element = driver.find_element(By.XPATH, '//a[contains(@href, "/explore/locations/")]')
        location = location_element.text
        details['location'] = location
    except:
        details['location'] = "Not Available"

    # Scrape post creation date
    try:
        date_element = driver.find_element(By.XPATH, '//time')
        post_date = date_element.get_attribute("datetime")  # This returns the date in ISO 8601 format
        details['post_date'] = post_date
    except:
        details['post_date'] = "Not Available"

    # Scrape comments
    comments = scrape_comments(driver, post_url)
    details['comments'] = comments

    return details

# Function to scrape bio and counts from profile page
def scrape_profile_info(driver, username):
    driver.get(f"https://www.instagram.com/{username}/")
    time.sleep(3)

    try:
        spans = driver.find_elements(By.CLASS_NAME, 'html-span')
        bio_element = driver.find_element(By.CSS_SELECTOR, 'span._ap3a._aaco._aacu._aacx._aad7._aade')

        if len(spans) >= 3:
            posts_count = spans[0].text
            followers_count = spans[1].text
            following_count = spans[2].text

            bio_text = bio_element.text
            clean_bio_text = clean_bio(bio_text)

            return {
                "posts_count": posts_count,
                "followers_count": followers_count,
                "following_count": following_count,
                "Bio": clean_bio_text
            }
    except:
        pass  # Ignore errors and continue

    return {}

# Read Instagram IDs from a CSV file
def read_instagram_ids_from_csv(file_path):
    instagram_ids = []
    try:
        with open(file_path, mode='r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                instagram_ids.append(row[0])  # Assuming usernames are in the first column
    except:
        pass  # Ignore errors and continue
    return instagram_ids

# Initialize WebDriver
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.instagram.com")

# Instagram login
time.sleep(5)
try:
    username_input = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')
    username_input.send_keys('satyasri849')

    password_input = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')
    password_input.send_keys('satyasriraghavu@123')

    login_button = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')
    login_button.click()

    # Wait for login to complete
    time.sleep(5)
except:
    pass  # Ignore errors and continue

# Read Instagram profiles from a CSV file
instagram_ids = read_instagram_ids_from_csv('foodbloggers.csv')  # Specify your CSV file name here

all_profiles_data = []

for username in instagram_ids:
    # Scrape profile information
    profile_data = scrape_profile_info(driver, username)

    # Scrape post URLs from the profile
    post_urls = scrape_profile_posts(driver, username)

    post_data = {}

    # Scrape details for each post
    for index, post_url in enumerate(post_urls[:10]):
        details = scrape_post_details(driver, post_url)
        post_data[f'post_{index + 1}'] = {
            "post_url": post_url,
            **details  # Include likes, hashtags, location, date, and comments
        }

    # Combine profile data and posts
    profile_data["posts"] = post_data
    profile_data["username"] = username

    all_profiles_data.append(profile_data)

    time.sleep(3)

# Save all profiles data to JSON
response_json = json.dumps(all_profiles_data, indent=4)

with open('instagram_profiles_full_data.json', 'w') as json_file:
    json_file.write(response_json)

print("Data saved to instagram_profiles_full_data.json")

# Close the WebDriver
driver.quit()
