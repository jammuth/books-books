import json
import os
import logging
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from xml.dom import minidom


log_date = datetime.now().strftime("%Y%m%d")
log_filename = f".\\logs\\app-{log_date}.log"
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def copy_src_file(kindle_cache_path="None", copy_of_xml_path="None"):
  src = kindle_cache_path
  dst = copy_of_xml_path

  if not os.path.exists(src):
    logging.error(f"Source file does not exist: {src}")
    return False
  else:
    if not os.path.exists(os.path.dirname(dst)):
      os.makedirs(os.path.dirname(dst))
      logging.info(f"Created directory for destination: {os.path.dirname(dst)}")
    with open(src, "rb") as fsrc, open(dst, "wb") as fdst:
      fdst.write(fsrc.read())
    logging.info(f"Copied {src} to {dst}")

  logging.info("Preload completed successfully.")
  return True

def convert_xml_to_json(src_file):
  last_sync_date = datetime.now()
  bookcount = 0
  books_purchased_in_last_sync = 0
  books_purchased_7_days = 0
  books_purchased_14_days = 0
  books_purchased_30_days = 0
  books_purchased_60_days = 0
  books_purchased_90_days = 0
  books_purchased_180_days = 0
  books_purchased_365_days = 0
  
  if not os.path.exists(src_file):
    logging.error(f"Source XML file does not exist: {src_file}")
    return None  
  try:
    tree = ET.parse(src_file)
    root = tree.getroot()
    jsondata = {"books": [], "summary": {}}
    for book in root.findall(".//meta_data"):
      book_info = {}
      book_info["title"] = book.find("title").text if book.find("title") is not None else "Unknown"
      #clean up title
            
      book_info["title"] = book_info["title"].replace("\n", "")
      book_info["title"] = book_info["title"].replace("\r", "")
      while "  " in book_info["title"]:
        book_info["title"] = book_info["title"].replace("  ", " ")
      book_info["title"] = book_info["title"].strip()
      
      # if the title doesnt contain at least one letter, skip it
      if not any(char.isalpha() for char in book_info["title"]):
        logging.warning(f"Skipping book with title '{book_info['title']}' as it does not contain any letters.")
        continue
      
      #book_info["author"] = book.find("author").text if book.find("author") is not None else "Unknown"
      book_info["authors"] = [author.text for author in book.find("authors").findall("author")] if book.findall("authors") else ["Unknown"]
      book_info["asin"] = book.find("ASIN").text if book.find("ASIN") is not None else "Unknown"
      book_info["asin"] = book_info["asin"].strip()
      book_info["amazon_link"] = f"https://www.amazon.co.uk/dp/{book_info['asin']}"
      
      logging.info(f"processing book {book_info['title']} with ASIN {book_info['asin']}")
      
      
      publication_date = book.find("publication_date").text if book.find("publication_date") is not None else "0000-00-00T00:00:00+0000"
      try:
        if publication_date == None:
          publication_date = datetime(month=0,year=0,day=0).strftime("%Y-%m-%dT%H:%M:%S+0000")
        else:
          # Parse the publication date string into a datetime object
          # Assuming the format is "YYYY-MM-DDTHH:MM:SS+0000"
          publication_date_obj = datetime.strptime(publication_date, "%Y-%m-%dT%H:%M:%S+0000")
      except ValueError:
        logging.error(f"Invalid date format: {publication_date}")
        continue
      
      
      purchase_date = book.find("purchase_date").text if book.find("purchase_date") is not None else datetime(month=0,year=0,day=0).strftime("%Y-%m-%dT%H:%M:%S+0000")
      try:
        if purchase_date == None:
          purchase_date = datetime(month=0,year=0,day=0).strftime("%Y-%m-%dT%H:%M:%S+0000")
        else:
          # Parse the purchase date string into a datetime object
          # Assuming the format is "YYYY-MM-DDTHH:MM:SS+0000"
          purchase_date_obj = datetime.strptime(purchase_date, "%Y-%m-%dT%H:%M:%S+0000")
      except ValueError:
        logging.error(f"Invalid date format: {purchase_date}")
        continue
      
      if purchase_date_obj > last_sync_date:
        books_purchased_in_last_sync += 1
      
      # Check if the purchase date is within the last 7, 14, 30, 60, 90, 180, or 365 days        
      if purchase_date_obj > datetime.now() - timedelta(days=7):
        books_purchased_7_days += 1
      if purchase_date_obj > datetime.now() - timedelta(days=14):
        books_purchased_14_days += 1
      if purchase_date_obj > datetime.now() - timedelta(days=30):
        books_purchased_30_days += 1
      if purchase_date_obj > datetime.now() - timedelta(days=60):
        books_purchased_60_days += 1
      if purchase_date_obj > datetime.now() - timedelta(days=90):
        books_purchased_90_days += 1
      if purchase_date_obj > datetime.now() - timedelta(days=180):
        books_purchased_180_days += 1
      if purchase_date_obj > datetime.now() - timedelta(days=365):
        books_purchased_365_days += 1
      
      #convert dates to string format
      book_info["publication_date"] = publication_date_obj.strftime("%Y-%m-%dT%H:%M:%S")
      book_info["purchase_date"] = purchase_date_obj.strftime("%Y-%m-%dT%H:%M:%S")
      
      book_info["id"] = book_info["asin"] + "_" + publication_date_obj.strftime("%Y%m%d%H%M%S")
      
      # look up book in jsondata["books"] to see if it already exists
      existing_book = next((b for b in jsondata["books"] if b["asin"] == book_info["asin"]), None)

      if existing_book is not None:
        logging.error(f"Duplicate Book Found {book_info['asin'], book_info['title']} already exists in JSON data")
        continue

      jsondata["books"].append(book_info)
      bookcount += 1
    # meta_data
    jsondata["summary"] = {
      "sync_date": last_sync_date.strftime("%Y-%m-%dT%H:%M:%S"),
      "books_processed": bookcount,
      "books_purchased_in_last_sync": books_purchased_in_last_sync,
      "books_purchased_7_days": books_purchased_7_days,
      "books_purchased_14_days": books_purchased_14_days,
      "books_purchased_30_days": books_purchased_30_days,
      "books_purchased_60_days": books_purchased_60_days,
      "books_purchased_90_days": books_purchased_90_days,
      "books_purchased_180_days": books_purchased_180_days,
      "books_purchased_365_days": books_purchased_365_days
    }
    
  except ET.ParseError as e:
    logging.error(f"Failed to parse XML: {e}")
    return None
  
  return jsondata

def save_json_file(jsondata):
  json_file_path = ".\\data\\kindle_cache_data.json"
  
  if not os.path.exists(os.path.dirname(json_file_path)):
    os.makedirs(os.path.dirname(json_file_path))
    logging.info(f"Created directory for JSON file: {os.path.dirname(json_file_path)}")
  
  with open(json_file_path, "w", encoding="utf-8") as json_file:
    json.dump(jsondata, json_file, indent=4, ensure_ascii=False)
  
  logging.info(f"Saved JSON data to {json_file_path}")
  return True

if __name__ == "__main__":
  logging.info("Starting the Kindle cache processing script. from loadFromKindleCache.py")
  kindle_cache_path = "C:\\Users\\james\\AppData\\Local\\Amazon\\Kindle\\Cache\\KindleSyncMetadataCache.xml"
  copy_of_xml_path = ".\\data\\copy_of_xml_file.xml"
  if copy_src_file(kindle_cache_path, copy_of_xml_path):
    jsondata = convert_xml_to_json(copy_of_xml_path)
    if jsondata is not None:
      save_json_file(jsondata)
  logging.info("Process completed successfully.")


