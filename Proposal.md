Requirements:
 - identifies your team members,
 - identify one or more standard or 3rd party libraries that you will investigate along with a website reference that describes the libraries,
 - and finally a short description about the goals of your proposed application.

# X-Post and Repost Analysis of reddit.com

## Members
Noah Bass (bassnh), Kristian Snyder (snyderks)

## Third Party Libraries

### ijson

[https://pypi.python.org/pypi/ijson/](https://pypi.python.org/pypi/ijson/)

ijson is used to read large JSON files without having to read the entire file into memory and can use a backend C parser to accelerate the rate of parsing, minimizing resource usage when parsing JSON.

### RQ

[http://python-rq.org](http://python-rq.org)

RQ or Redis Queue is used to create jobs that are processed by separate workers, allowing for a basic implementation of splitting tasks and performing them in parallel.

### NetworkX

[https://networkx.github.io](https://networkx.github.io)

NetworkX is a graph library allowing for the creation of several types of graphs and can perform various graph algorithms on them, allowing for quick graph building, manipulation, and viewing.

## Goals

Using available reddit data, the application will create a visualization of a subset of posts on the site that were reposted in a short period of time between different subreddits—called x-posting if the user is the same or if the post is explicitly referenced to be originally from a different subreddit. This allows for analysis of where heavily reposted submissions originate, where one submission may get the majority of its upvotes from, and which posts die quickly, meaning they either command a low amount of votes or are downvoted to or below 0.
