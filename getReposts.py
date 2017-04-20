"""GetReposts takes an array of submissions and writes to disk all those with duplicate URLs."""

import ijson.backends.yajl2 as ijson
import json
import sys
import re

def getDupes(filename, outfile):
    """Find all the duplicates within the submissions.
    Writes the links to a file.
    """
    try:
        links = set()
        dupes = set()
        i = 0
        w = open(outfile, "w")
        w.write("[")
        dupLen = 0
        r = re.compile("((http|https):\/\/|\/r\/)(.+?)($|\?)", re.IGNORECASE)
        for item in ijson.items(open(filename, "rb"), "item"):
            # get the base path of the url
            base = r.search(item["url"])
            if base == None:
                print(item["url"])
            else:
                u = base.group(3).lower()
                if u in links and u not in dupes:
                    dupes.add(u)
                    json.dump(item, w)
                    w.write(",\n")
                    dupLen += 1
                else:
                    links.add(u)
            i += 1
            if i % 10000 == 0:
                print("Read", i, "items")

        w.seek(w.tell()-2)
        w.write("]")
        print(dupLen, "reposts")
    except:
        import traceback
        print(traceback.format_exc())

getDupes("shortened08.json", "links.json")
