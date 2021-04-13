import os
import sys
import urllib
import re
import time
import requests
import mimetypes
import traceback

from pathlib import Path
p = Path(__file__).resolve().parents[2]
sys.path.insert(1, str(p) + '/common')

# from file_downloaders.downloaders import get_doc, get_pdf, get_xls
from base_scrapers.file_downloaders.downloaders import get_doc, get_pdf, get_xls

def get_files(save_dir, sleep_time, delete=True, debug=False, name_in_url=False, try_overwite=False, domain_included=False, no_overwrite=False):
    name_in_url = name_in_url
    if not os.path.isfile("url_name.txt"):
        return

    with open("url_name.txt", "r") as input_file:
        for line in input_file:
            print(line)

            line_list = line.split(", ")
            url_2 = line_list[0]
            file_name = line_list[1].replace(" ", "_")[:-1]
            # file_name = save_dir + file_name
            # document = requests.get(url_2, allow_redirects=True)
            response = requests.get(url_2)
            content_type = response.headers['content-type']
            extension = mimetypes.guess_extension(content_type)

            # If the name IS in the url
            if name_in_url == True:
                if ".pdf" in extension:
                    # save_path = os.path.join(save_dir, file_name+".pdf")
                    print(file_name)
                    get_pdf(save_dir, file_name, url_2, debug, sleep_time, try_overwite, no_overwrite)
                    print(sleep_time)

                elif ".doc" in extension:
                    get_doc(save_dir, file_name, url_2, sleep_time)

                elif ".xls" in extension:
                    get_xls(save_dir, file_name, url_2, sleep_time)

                else:
                    print("Unhandled documents type")
                    print("Url: " + url_2)

            # If the name is NOT in the url
            else:
                import cgi
                if not debug:
                    response = urllib.request.urlopen(url_2)
                    file_name, params = cgi.parse_header(response.headers.get('Content-Disposition', ''))
                    if "=" in file_name:
                        file_name = file_name.split("=")
                    elif ":" in file_name:
                        filename = file_name.split(":")
                    file_name = file_name[1].strip("\"")

                if debug:
                    response = urllib.request.urlopen(url_2)
                    print(response)
                    file_name, params = cgi.parse_header(response.headers.get('Content-Disposition', ''))
                    print("file_name: " + str(file_name) + ", params: " + str(params))
                    if "=" in file_name:
                        file_name = file_name.split("=")
                    elif ":" in file_name:
                        filename = file_name.split(":")
                    print(file_name)
                    file_name = file_name[1].strip("\"")
                    print(file_name)

                if ".pdf" in extension:
                    # save_path = os.path.join(save_dir, file_name+".pdf")
                    print(file_name)
                    get_pdf(save_dir, file_name, url_2, debug, sleep_time, try_overwite)

                elif ".doc" in extension:
                    get_doc(save_dir, file_name, url_2, sleep_time)

                elif ".xls" in extension:
                    get_xls(save_dir, file_name, url_2, sleep_time)

                else:
                    print("Unhandled documents type")
                    print("Url: " + url_2)

    input_file.close()

    # Used for debugging
    if delete != False:
        os.remove("url_name.txt")
