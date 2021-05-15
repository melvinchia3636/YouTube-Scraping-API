.. _quickstart:

Quickstart
==========

Although using Youtube Scraping API is simple enough, but some tutorials are still needed.
This guide will walk you through the basic usage of Youtube Scraping API.

Let’s get started with some examples, I mean a lot of examples.

Initialize
----------
To use a library, first of all you need to import it, no doubt for that. To import Youtube Scraping API, all you need is one line of code:

.. code-block:: python

	>>> from youtube_scraping_api import YoutubeAPI

Personally speaking, the name of the library is a little bit long, but unfortunately we have no choice. When the developer was registering this library on PyPi, all other names like 'youtube-api', 'youtube-scraper' have all been taken by others. Maybe there are some ways to make the name shorter, we can only hope that the developer can figure it out as soon as possible.

Let's get back to the point. Now how can you start using it after import? That's a good question, but the answer is stupidly simple: call the class. Here is how you can do it:

.. code-block:: python

	>>> api = YoutubeAPI()

Here you go! Initialization completed. Now you're all set to do whatever the heck you want with this API. But please don't DDOS lol,  I'm not sure if you'll get arrested by FBI (just kidding) if you do so.

Search
------
Tired of searching on YouTube webpage? Or you just wanna try to be cool? We have the perfect solution for you. With this API, you can do basically everything you can perform on youtube webpage by using codes. Sounds cool, right? Let's try searching for your favourite videos, channel, or playlist:

.. code-block:: python

	>>> query = 'Minecraft Survival Guide'
	>>> api.search(query)

The output of these two lines of codse should be something like:

.. code-block:: powershell

	<SearchResult {'Playlist': 3, 'Video': 16, 'Channel': 1, 'Shelf': 1}>

So you'll probably ask: What is this? Where is my result? So let me tell you: this thing is just a wrapper. The real result is inside this wrapper. This is a special datatype that inherits from Python builtin list, so what you can do is:

.. code-block:: python

	>>> for result in api.search(query):
	... 	print(result)

And now you should be able to see all results get printed out one by one. For more information on types of result, check out :ref:`API Reference <api reference>`.

Video
-----

Playlist
--------

Channel
-------