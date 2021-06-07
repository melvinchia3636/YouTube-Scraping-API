.. Youtube Scraping API documentation master file, created by
   sphinx-quickstart on Thu May 13 07:32:07 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Youtube Scraping API
====================
.. image:: https://img.shields.io/readthedocs/youtube-scraping-api
  :alt: Docs
.. image:: https://img.shields.io/pypi/v/youtube-scraping-api
  :alt: Pypi
  :target: https://pypi.python.org/pypi/youtube-scraping-api/
.. image:: https://img.shields.io/pypi/pyversions/youtube-scraping-api.svg
  :alt: Python Versions
  :target: https://pypi.python.org/pypi/youtube-scraping-api/
.. image:: https://img.shields.io/pypi/l/youtube-scraping-api
  :alt: License
  :target: https://github.com/melvinchia3636/YouTube-Scraping-API/blob/main/LICENSE
.. image:: https://img.shields.io/github/last-commit/melvinchia3636/Youtube-Scraping-API
  :alt: Last Commit
  :target: https://github.com/melvinchia3636/YouTube-Scraping-API
.. image:: https://img.shields.io/github/repo-size/melvinchia3636/YouTube-Scraping-API
  :alt: Repo Size
  :target: https://github.com/melvinchia3636/YouTube-Scraping-API
  

**Youtube Scraping API** is a lightweight, easy-to-use library packed with Youtube data scraper and video downloader. This scraping api doesn't depend on Youtube Official API, since there are strict quota when using it. With this API, you can get access to all data of **Youtube videos**, **playlists**, **channels**, and **search results**. Simply download the package using pip, and you're ready to go. For those who never use this API before, :ref:`Quickstart Guide <quickstart>` can help you get started with using this API quickly.

Here is a simple demonstration

.. code-block:: python

   from youtube_scraping_api import YoutubeAPI
   api = YoutubeAPI()

   #search for videos, playlists, channels, and etc.
   api.search('python tutorial')

   #download videos
   api.video('a1EYnngNHIA').download()
   
Of course these are just a tip of the iceberg. We have a lot more features available in this API.

Features
--------
* Scrape YouTube search results
* Scrape YouTube suggestion queries
* Useful filters for YouTube searching
* Download videos with any resolutions
* Get metadata of channels, videos, and playlists
* Scrape thumbnail urls of videos, channels, and playlists
* Scrape captions of videos
* Ability to log progress when executing code
* Nicely formed object structure
* Welly documented source code
* You can literally create a fully working YouTube clone with this API :)

Todo
----
* Callback function for video downloading
* Unit test for each features
* Ability to merge high quality videos and sound
* Turn video download data into object
* Extract from channel:
   * all videos
   * all playlist
   * channel page
   * community posts
   * all external links in about page
   * sections in channel homepage
* Search results filtering system
* Search results sorting system

.. toctree::
   :maxdepth: 9999
   :caption: Contents:

   installation
   quickstart
   API reference

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`