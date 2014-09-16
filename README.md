Feed Logger
===========

`feed_logger.py` is a python script that fetches feeds and stores them in git allowing you to inspect the differnece over time. It is currently very JSON specific, but is intended to be a good base to build on.

`feeds.json` is a simple dictionary containing the feeds to fetch. The key is used to name the directory for each result.


Installation
------------
1. Clone this repro
2. Edit `feeds.json`

That's it. The script uses it's own git repo to store the feeds changes. Use your favorite git tools to view the changes over time.

Usage
-----
The `feed_logger.py` script take no arguments and is intended to be used in a `crontab`. It can, of course, be called manuualy, in a `while`/`for` loop, or queued with `at`, etc.

After running the script for at least 2 cycles, you can inspect the changes with a simple call to `git log -u --color-words` or use your favorite GUI tool.
