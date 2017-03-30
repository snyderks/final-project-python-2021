# X-Post and Repost Analysis

## Libraries
RQ (Redis Queue) for threading, NetworkX for graph display

## Summary
 - Analyze Reddit submissions
 - Determine which posts were reposted
 - Find the original post for that month/year (depending on processing)
 - Compare vote counts (normalized by subscribers), user ids (to see if it was the same user)
 - Create a graph of posts that were reposted and their path through Reddit
