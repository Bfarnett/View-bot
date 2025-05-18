import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import random

WATCH_MIN = 60
WATCH_MAX = 150

CHANNEL_URLS = [
    "https://youtube.com/@mchvisuals?si=oHiWVeHYTD4TIe_3",
    "https://youtube.com/@mchvisuals?si=oHiWVeHYTD4TIe_3",
    "https://youtube.com/@mchvisuals?si=oHiWVeHYTD4TIe_3",
    "https://youtube.com/@mchvisuals?si=oHiWVeHYTD4TIe_3",
    "https://youtube.com/@mchvisuals?si=oHiWVeHYTD4TIe_3"
]

driver = uc.Chrome()

def reject_cookies():
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//button[.//span[text()='Reject all']]"))
        )
        reject_btn = driver.find_element(By.XPATH, "//button[.//span[text()='Reject all']]")
        driver.execute_script("arguments[0].scrollIntoView(true);", reject_btn)
        time.sleep(1)
        reject_btn.click()
        time.sleep(2)
    except TimeoutException:
        pass

def watch_random_video_from_channel(url):
    driver.get(url)
    reject_cookies()

    try:
        videos_tab = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//tp-yt-paper-tab//div[contains(text(), 'Videos')]"))
        )
        videos_tab.click()
        time.sleep(3)
    except TimeoutException:
        print("Could not switch to Videos tab.")

    driver.execute_script(f"window.scrollBy(0, {random.randint(800, 1600)});")
    time.sleep(2)

    video_links = driver.find_elements(By.XPATH, "//a[@id='video-title' or contains(@href, '/shorts/')]")

    if not video_links:
        print("No videos found on this channel.")
        return

    video = random.choice(video_links)
    title = video.get_attribute("title") or video.get_attribute("href")
    print(f"Selected: {title}")
    driver.execute_script("arguments[0].scrollIntoView(true);", video)
    time.sleep(random.uniform(1, 2))
    driver.execute_script("arguments[0].click();", video)

    watch_time = random.randint(WATCH_MIN, WATCH_MAX)
    print(f"Watching for {watch_time} seconds...")
    for _ in range(watch_time // 10):
        time.sleep(10)
        driver.execute_script(f"window.scrollBy(0, {random.randint(50, 300)});")

# === Runtime Logic ===
start_time = time.time()
daily_limit_seconds = random.randint(8 * 3600, 10 * 3600)  # 8–10 hours
views_today = 0
next_rest_after = random.randint(5, 7)

while True:
    elapsed = time.time() - start_time
    if elapsed >= daily_limit_seconds:
        print("Daily time limit reached. Shutting down.")
        break

    print(f"\nView {views_today + 1} (elapsed: {round(elapsed / 60)} min / {daily_limit_seconds // 60} min limit)")
    channel_url = random.choice(CHANNEL_URLS)
    print(f"Visiting channel: {channel_url}")
    watch_random_video_from_channel(channel_url)
    views_today += 1

    if views_today % next_rest_after == 0:
        rest_time = random.randint(600, 1200)  # 10–20 minutes
        print(f"Long rest for {rest_time // 60} minutes after {views_today} views...")
        time.sleep(rest_time)
        next_rest_after = random.randint(5, 7)

    else:
        cooldown = random.randint(10, 30)
        print(f"Cooldown for {cooldown} seconds...\n")
        time.sleep(cooldown)

print("Bot finished for the day.")
driver.quit()
