import logging
import datetime
from loadFromKindleCache import copy_src_file,convert_xml_to_json,save_json_file
from firebase_database import FirestoreDB

log_date = datetime.datetime.now().strftime("%Y%m%d")
log_filename = f".\\logs\\app-{log_date}.log"
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

kindle_cache_path = "C:\\Users\\james\\AppData\\Local\\Amazon\\Kindle\\Cache\\KindleSyncMetadataCache.xml"
copy_of_xml_path = ".\\data\\copy_of_xml_file.xml"

def main():
  if copy_src_file(kindle_cache_path, copy_of_xml_path):
    jsondata = convert_xml_to_json(copy_of_xml_path)
    if jsondata != None:
      db = FirestoreDB()
      id = db.add_item(jsondata)
      logging.info(f"Data uploaded to Firestore with document ID: {id}")
      save_json_file(jsondata)
      

if __name__ == "__main__":
  main()
  logging.info("Process completed successfully.")