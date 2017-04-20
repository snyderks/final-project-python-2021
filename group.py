"""Group submissions by url in a sorted fashion"""

import json

def group(filename, outfile):
    """Takes submissions from filename and groups them by url.
    Result is written to outfile in json."""

    grouped_submissions = dict()
    links_file = open(filename, 'r')
    links = json.loads(links_file.read())
    
    for item in links:
        if item['url'] not in grouped_submissions:
            # this url does not yet exist in grouped_submissions, so add it as a new set
            # grouped_submissions[item['url']] = 'foo'
            grouped_submissions[item['url']] = set()
        grouped_submissions[item['url']].add(item['name'])
    
    # sort the keys in grouped_submissions

group('links.json', 'links-groups.json')
