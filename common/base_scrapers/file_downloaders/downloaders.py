import os
import sys
import urllib
import re
import time
import requests
import mimetypes
import traceback
import filecmp
from datetime import date


def file_compare(save_dir, file_1, file_2, no_overwrite=False):
    file_1 = save_dir + file_1
    file_2 = save_dir + file_2

    compared = filecmp.cmp(file_1, file_2)

    if compared == True:
        print("File has not changed")
        # Not sure why I didn't just use `file_2`
        changed_file = file_2
        os.remove(changed_file)
    else:
        # I tried to just put the code to write it here, but it would've required too many arguments
        print("File has changed")
        return False


def get_pdf(
    save_dir, file_name, url_2, debug, sleep_time, try_overwite, no_overwrite=False
):
    file_name = file_name.lstrip("/")
    print(file_name)
    if os.path.exists(save_dir + file_name) == False:
        try:
            pdf = urllib.request.urlopen(url_2.replace(" ", "%20"))
        except urllib.error.HTTPError:
            print("HTTP Error 404: Not Found")
            print("URL: " + str(url_2))
            print("")
            if debug:
                traceback.print_exc()
            sys.exit()

        with open(save_dir + file_name, "wb") as file:
            file.write(pdf.read())
        file.close()

        time.sleep(sleep_time)
        print("Sleep")
    elif os.path.exists(save_dir + file_name) == True and try_overwite == True:
        try:
            pdf = urllib.request.urlopen(url_2.replace(" ", "%20"))
        except urllib.error.HTTPError:
            print("HTTP Error 404: Not Found")
            print("")
            print("URL: " + str(url_2))
            if debug:
                traceback.print_exc()
            sys.exit()
        print("Comparing")

        # Saves the pdf while prepending with "new_"
        with open(save_dir + "new_" + file_name, "wb") as file:
            file.write(pdf.read())
        file.close()

        new_filename = "new_" + file_name

        # Compares the file using file_compare, which will remove the
        file_compare(save_dir, file_name, new_filename)
        time.sleep(sleep_time)

    # If the file exists, and no_overwrite is true, then:
    elif os.path.exists(save_dir + file_name) == True and no_overwrite == True:
        # Tries to get the file and set it to pdf
        try:
            pdf = urllib.request.urlopen(url_2.replace(" ", "%20"))
        except urllib.error.HTTPError:
            print("HTTP Error 404: Not Found")
            print("")
            print("URL: " + str(url_2))
            if debug:
                traceback.print_exc()
            sys.exit()
        print("Comparing")

        # Saves the pdf while prepending with "new_"
        with open(save_dir + "new_" + file_name, "wb") as file:
            file.write(pdf.read())
        file.close()
        new_filename = "new_" + file_name

        if file_compare(save_dir, file_name, new_filename, no_overwrite=True) == True:
            date_name = date.today()
            print(date_name)
            file_name = (
                file_name.strip(".pdf")
                + "_"
                + str(date_name).replace("-", "_")
                + ".pdf"
            )
            print(file_name)

            with open(save_dir + file_name, "wb") as file:
                file.write(pdf.read())
            file.close()


def get_xls(save_dir, file_name, url_2, sleep_time, debug):
    if ".xls" not in file_name:
        # Allows saving as xls even if it's not in the file_name (saves in proper format)
        file_name = file_name + ".xls"
    if os.path.exists(save_dir + file_name) == False:
        try:
            pdf = urllib.request.urlopen(url_2.replace(" ", "%20"))
        except urllib.error.HTTPError:
            print("HTTP Error 404: Not Found")
            print("URL: " + str(url_2))
            print("")
            if debug:
                traceback.print_exc()
            exit()
        with open(save_dir + file_name, "wb") as file:
            file.write(pdf.read())
        file.close()
        time.sleep(sleep_time)
        print("Sleep")


def get_doc(save_dir, file_name, url_2, sleep_time):
    if os.path.exists(save_dir + file_name) == False:
        document = requests.get(url_2.replace(" ", "%20", allow_redirects=True))
        with open(file_name, "w") as data_file:
            data_file.write(document.text)  # Writes using requests text 	function thing
        data_file.close()
        time.sleep(sleep_time)
        print("Sleep")
