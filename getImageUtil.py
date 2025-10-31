import requests
from bs4 import BeautifulSoup
import re

def getImageFromAsin(ASIN):
  if not ASIN:
    print("No ASIN provided.")
    return

  headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
  }

  url = "https://www.amazon.co.uk/dp/" + ASIN
  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.text, "html.parser")

  # Amazon often stores image data in a JSON inside a script tag
  scripts = soup.find_all("script")
  image_urls = set()

  for script in scripts:
    if script.string and "ImageBlockATF" in script.string:
      matches = re.findall(r'"hiRes":"(https://[^"]+)"', script.string)
      image_urls.update(matches)
      # matches = re.findall(r'"large":"(https://[^"]+)"', script.string)
      # image_urls.update(matches)
  if not image_urls:
    # Fallback: look for img tags in the main image block
    main_image_block = soup.find(id="main-image-container")
    if main_image_block:
      imgs = main_image_block.find_all("img")
      for img in imgs:
        src = img.get("src")
        if src and src.startswith("https://m.media-amazon.com/images/I/"):
          image_urls.add(src)

  print("Landing images found:")
  for url in image_urls:
    print(url.replace("_SL1500_.jpg", "jpg"))