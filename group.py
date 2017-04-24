"""Group submissions by url in a sorted fashion."""

import json
import re

def group(filename, outfile):
    """Take submissions from filename and group them by url.
    Write result to outfile in json.
    """
    grouped_submissions = dict()
    links_file = open(filename, 'r')
    links = json.loads(links_file.read())
    r = re.compile("((http|https):\/\/|\/r\/)(.+?)($|\?)", re.IGNORECASE)

    for item in links:
        url = r.search(item["url"]).group(3).lower()
        if url not in grouped_submissions:
            # this url does not yet exist in grouped_submissions, so add it as a new set
            # grouped_submissions[item['url']] = 'foo'
            grouped_submissions[url] = []
        grouped_submissions[url].append(item)

    # sort the keys in grouped_submissions by date
    for key, value in grouped_submissions.items():
        grouped_submissions[key] = sorted(value, key=lambda x: x["created"])

    # write to the file
    w = open(outfile, "w")
    json.dump(grouped_submissions, w)

group('links.json', 'links-groups.json')
