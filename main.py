import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def download_images(search_query="Shubhman Gill", num_images=50, save_dir="images"):
    # Create folder
    save_path = os.path.join(save_dir, search_query.replace(" ", "_"))
    os.makedirs(save_path, exist_ok=True)

    # Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # comment out to see the browser
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Open Bing Images
    search_url = f"https://www.bing.com/images/search?q={search_query.replace(' ', '+')}&form=HDRSC2"
    driver.get(search_url)
    time.sleep(2)

    # Scroll to load more images
    for _ in range(8):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5)

    # Find image elements
    thumbnails = driver.find_elements(By.CSS_SELECTOR, "a.iusc")
    print(f"Found {len(thumbnails)} thumbnails on Bing.")

    count = 0
    for thumb in thumbnails:
        try:
            m = thumb.get_attribute("m")
            # Extract the m attribute containing the image URL
            if m:
                import json
                m_json = json.loads(m)
                img_url = m_json.get("murl")
                if img_url:
                    img_data = requests.get(img_url, timeout=5).content
                    file_path = os.path.join(save_path, f"{search_query}{count+1}.jpg")
                    with open(file_path, "wb") as f:
                        f.write(img_data)
                    count += 1
                    print(f"✅ Downloaded {count}")
            if count >= num_images:
                break
        except Exception as e:
            print("⚠️ Error:", e)
            continue

    driver.quit()
    print(f"\n🎉 Done! {count} images of {search_query} saved in '{save_path}'")

if __name__ == "__main__":
    download_images("Shubhnam Gill", num_images=50)
