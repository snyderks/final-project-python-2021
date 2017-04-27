"""GetReposts takes an array of submissions and writes to disk all those with duplicate URLs."""

# requires yajl if increased performance is desired.
# if not, comment out the yajl import and uncomment the below line:
# import ijson
# everything will function identically (in this case. YAJL acts slightly differently,
# as it is a JSON parser written in C with its own restrictions.)
import ijson.backends.yajl2 as ijson
import json
import re

def getDupes(filename, outfile):
    """Find all the duplicates within the submissions.
    Writes the links to a file.
    """
    try:
        links = set()
        dupes = set()
        i = 0
        dupLen = 0
        # split the url into components
        # looking for everything after http://
        # but before any queries, e.g. ?ref=google.com, since these can
        # vary but still result in the same page
        r = re.compile("((http|https):\/\/|\/r\/)(.+?)($|\?)", re.IGNORECASE)
        # first get all the duplicate links
        for item in ijson.items(open(filename, "rb"), "item"):
            # get the base path of the url
            base = r.search(item["url"])
            if base == None:
                print(item["url"])
            else:
                # select the correct portion of the url
                # lowercase convert for case insensitive matching
                u = base.group(3).lower()
                if u in links and u not in dupes:
                    dupes.add(u)
                    dupLen += 1
                else:
                    links.add(u)
            i += 1
            if i % 10000 == 0:
                # shows progress of reading through the file,
                # since this process can take a little while.
                print("Read", i, "items")

        w = open(outfile, "w")
        w.write("[")
        # now read back through the file again, and pull out all the
        # submissions with links that were marked as duplicates
        for item in ijson.items(open(filename, "rb"), "item"):
            # get the base path of the url
            base = r.search(item["url"])
            if base is not None:
                # select the correct portion of the url
                # lowercase convert for case insensitive matching
                u = base.group(3).lower()
                if u in dupes:
                    json.dump(item, w)
                    w.write(",\n")
                    dupLen += 1
        w.seek(w.tell()-2)
        w.write("]")
    except:
        import traceback
        print(traceback.format_exc())

getDupes("shortened08.json", "links.json")
