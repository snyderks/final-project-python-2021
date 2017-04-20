"""GetReposts takes an array of submissions and writes to disk all those with duplicate URLs."""

import ijson.backends.yajl2 as ijson
import json
import sys

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
        for item in ijson.items(open(filename, "rb"), "item"):
            if item["url"] in links and item["url"] not in dupes:
                dupes.add(item["url"])
                json.dump(item, w)
                w.write(",\n")
                dupLen += 1
            else:
                links.add(item["url"])
            i += 1
            if i % 10000 == 0:
                print("Read", i, "items")

        w.seek(w.tell()-2)
        w.write("]")
        print(dupLen, "reposts")
    except:
        print(sys.exc_info()[1])

getDupes("shortened08.json", "links.json")
