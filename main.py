from loadFromKindleCache import copy_src_file,convert_xml_to_json,save_json_file
import logging

logging.basicConfig(level=logging.INFO)

kindle_cache_path = "C:\\Users\\james\\AppData\\Local\\Amazon\\Kindle\\Cache\\KindleSyncMetadataCache.xml"
copy_of_xml_path = ".\\data\\copy_of_xml_file.xml"

def main():
  if copy_src_file(kindle_cache_path, copy_of_xml_path):
    jsondata = convert_xml_to_json(copy_of_xml_path)
    if jsondata != None:
      save_json_file(jsondata)

if __name__ == "__main__":
  main()
  logging.info("Process completed successfully.")