# bluesky
A simple python tool for discovering accounts that are "popular" with accounts you already follow.

The tool generates two rankings:
1. Top accounts by number of their followers that are accounts you follow.
2. Top accounts by share of their followers made up of accounts you follow.

In both cases, your own account and any accounts you follow are excluded from the rankings, since the goal is to discover *new* accounts to follow.

The second ranking (by share) is necessary to exclude accounts with massive follower counts that are popular among your follows only because they're very popular *overall*.  The ranking by share, by contract, attempts to identify accounts that are *especially* popular among the accounts you already follow.

### Requirements:

* python3
* the `requests` package

If you have a working python3 environment, then you can install `requests` with:

`pip install requests`

### Options:

See valid usage and options with:
`python bluesky.py --help`

| Options | Description |
|---------|-------------|
|number_to_show|The number of rows in the two rankings by count and share|
|global_follower_threshold|The minimum number of followers an account must have in order to appear in the ranking by share|
|local_follower_threshold|The minimum number of followers an account must have *from among the accounts you follow* in order to appear in the ranking by share|

### Sample Output:

```
python bluesky.py -n 5 jayphoward.bsky.social
Loading accounts followed by the 52 accounts you follow:
...completed loading follows for 10 accounts
...completed loading follows for 20 accounts
...completed loading follows for 30 accounts
...completed loading follows for 40 accounts
...completed loading follows for 50 accounts

28: kenwhite.bsky.social (Domestic Enemy Hat)
28: chrislhayes.bsky.social (Chris Hayes)
24: jamellebouie.net (jamelle)
22: kevinmkruse.bsky.social (Kevin M. Kruse)
22: washingtonpost.com (The Washington Post)

Loading 507 account profiles:
...completed loading 100 account profiles
...completed loading 200 account profiles
...completed loading 300 account profiles
...completed loading 400 account profiles
...completed loading 500 account profiles

0.0198: stanveuger.bsky.social (Stan Veuger)
0.0126: willrinehart.bsky.social (Will Rinehart)
0.0112: sethamandel.bsky.social (Seth Mandel)
0.0103: basilhalperin.bsky.social (Basil Halperin)
0.0093: danielzhao.bsky.social (Daniel Zhao)
```