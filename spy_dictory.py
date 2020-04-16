from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36",
}


def worker(position, file_handler):
    response = requests.get(
        "https://www.collinsdictionary.com/browse/english/words-starting-with-{}".format(chr(position)),
        headers=headers)
    soup_pbj = BeautifulSoup(response.text, "html.parser")
    ul_obj = soup_pbj.find("ul", attrs={"class": "columns2"})
    for li in ul_obj:
        a = li.find("a")
        if a == -1:
            continue
        detailed_info = requests.get(url=a.get("href"), headers=headers)
        soup_pbj = BeautifulSoup(detailed_info.text, "html.parser")
        ul_obj_2 = soup_pbj.find("ul", attrs={"class": "columns2"})
        for li_2 in ul_obj_2:
            a2 = li_2.find("a")
            if a2 == -1:
                continue
            print(a2.text)
            file_handler.write("%s\n" % a2.text)


def collins(file_handler):
    t = ThreadPoolExecutor(max_workers=20)
    for i in range(ord("a"), ord("z") + 1):
        t.submit(worker, i, file_handler)
    t.shutdown()


if __name__ == '__main__':
    try:
        f = open("dictionary.txt", "a", encoding="utf-8")
        collins(f)
    except Exception as e:
        print(e)
    finally:
        f.close()
