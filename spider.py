import sys
import os
import requests
import shutil
from bs4 import BeautifulSoup

OPTIONS = ["r", "l", "p"]
VALID_IMG_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]

def crawl_img_links_from_url(url, limit=5):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    all_imgs = soup.find_all("img", limit=limit)
    img_links = []
    for image in all_imgs:
        img_links.append(image["src"])
    return img_links

def download_img_from_link(link, path="./data/"):
    if not os.path.exists(path):
        os.mkdir(path)
    response = requests.get(link, stream=True)
    img_name = link.split("/")[-1]
    is_extension_valid = False
    for img_ext in VALID_IMG_EXTENSIONS:
        if img_ext in img_name:
            is_extension_valid = True
            break
    if not is_extension_valid:
        print("Image extension is not valid")
        return False
    if os.path.exists(f"{path}{img_name}"):
        print("A file with that name already exists on the given path")
        return False
    if response.status_code == 200:
        with open(f"{path}{img_name}", "wb") as file: 
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, file)
    if os.path.exists(f"{path}{img_name}"):
        print("File downloaded succesfully")
        return True

def main():
    if len(sys.argv) < 2:
        print("""
Usage: ./spider.py [-rlpS] URL

    \033[1m-r\033[0m
        Recursively downloads the images in a URL received as a parameter.
    \033[1m-r -l [int]\033[0m
        Indicates the maximum depth level of the recursive download. If not indicated, it will be 5.
    \033[1m-p\033[0m
        Indicates the path where the downloaded files will be saved. If not specified, ./data/ will be used.
              """)
        sys.exit(1)
    if len(sys.argv) > 2:
         for index, arg in enumerate(sys.argv):
            if index == 0:
                continue
            if arg[0] == "-":
                if len(arg) > 2:
                    print("Please use flags separately")
                    sys.exit(1)
                else:
                    if "p" in arg:
                        if len(sys.argv[index+1:]) < 2:
                            print("PATH or URL were not specified")
                            sys.exit(1)
                        img_links = crawl_img_links_from_url(sys.argv[index+2])
                        for link in img_links:
                            download_img_from_link(link, path=sys.argv[index+1])
    else:
        img_links = crawl_img_links_from_url(sys.argv[1])
        for link in img_links:
            download_img_from_link(link)
    

if __name__ == "__main__":
    main()
