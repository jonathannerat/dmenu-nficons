#!/usr/bin/env python
from bs4 import BeautifulSoup
import requests
import os
import sys


def main():
    url = "https://www.nerdfonts.com/cheat-sheet"

    iconscsv = sys.argv[1] if len(sys.argv) > 2 else None
    if not iconscsv:
        folder = os.getenv("XDG_CACHE_HOME") or os.getenv("HOME") or "."
        iconscsv = folder + "/nficons.csv"

    if os.path.isfile(iconscsv):
        print("File already generated, you can now run dmenu-nficons")
        return

    soup = None

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    cheatsheet = soup.find(id = 'glyphCheatSheet')

    if cheatsheet is None:
        print("No cheatsheet found.", file=sys.stderr)
        return

    with open(iconscsv, "w") as fp:
        fp.write("id,name,icon\n")
        for i, iconelem in enumerate(cheatsheet.find_all(class_="column")):
            name = iconelem.find(class_="class-name").text
            codepoint = iconelem.find(class_="codepoint").text

            fp.write(f"{i},{name},{chr(int(codepoint, 16))}\n")


if __name__ == '__main__':
    main()
