# X-Post and Repost Analysis of reddit.com

## Members
Noah Bass (noahbass), Kristian Snyder (snyderks)

## Goals

Using available reddit data, the application will:
 - Analyze a set of Reddit submissions, such as all posts in a specific month.
 - Then determine which submissions were reposted or x-posted. X-posting is a specific form of reposting wherein the original subreddit is explicitly stated, usually in the title.
 - Analyze the submissions and group them by what link they point to, then comparing:
     - The relative popularity of the posts, based on vote count. This raw count will be weighted by subscriber count, to avoid giving prevalence to submissions in larger subreddits.
     - Any growth or regression in exposure of the specific link as it traverses reddit
     - Whether users are submitting to many subreddits at once, in a firehose technique, reposting to another place after little popularity in the original location, x-posting other users' popular content, or other patterns. These have well-defined patterns and are easy to recognize.
 - Finally, compiles the set of categorized and analyzed posts into a set of networks or graphs that are then interactively displayed to the user, so that they can highlight one group of posts, see the most popular by subreddit, and locate other interesting features of the data.

## Third Party Libraries and Resources

### ijson

[https://pypi.python.org/pypi/ijson/](https://pypi.python.org/pypi/ijson/)

ijson is used to read large JSON files without having to read the entire file into memory and can use a backend C parser to accelerate the rate of parsing, minimizing resource usage when parsing JSON.

### RQ

[http://python-rq.org](http://python-rq.org)

RQ or Redis Queue is used to create jobs that are processed by separate workers, allowing for a basic implementation of splitting tasks and performing them in parallel.

### NetworkX

[https://networkx.github.io](https://networkx.github.io)

NetworkX is a graph library allowing for the creation of several types of graphs and can perform various graph algorithms on them, allowing for quick graph building, manipulation, and viewing.

### files.pushshift.io

[http://files.pushshift.io/reddit/](http://files.pushshift.io/reddit/)

A collection of data scraped from reddit's public web API, freely available to the community for consumption and analysis.

### Managing scientific simulations with Python with RQ

[https://www.youtube.com/watch?v=Ttw816mwnQY](https://www.youtube.com/watch?v=Ttw816mwnQY)

A conference talk at PyCon AU about how to scale data processing in Python across multiple machines to take advantage of all available computing power.
