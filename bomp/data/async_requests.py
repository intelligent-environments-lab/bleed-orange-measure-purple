# -*- coding: utf-8 -*-
import aiohttp
import asyncio

from aiohttp import connector

# import requests

# Use nest_asyncio if iPython is detected in order to work with the existing event loop.
try:
    __IPYTHON__
except NameError:
    NESTED = False
else:
    NESTED = True

if NESTED:
    import nest_asyncio

MAX_CONNECTIONS = 100
TIMEOUT = 3600  # Override the default aiohttp session timeout of 300 seconds


class AsyncRequest:

    # This is the method that actually retrieves the data.
    @staticmethod
    async def __fetch_url(session, url, payload=None):
        if payload is not None:
            async with await session.post(url, data=payload) as resp:
                result = await resp.text()
        else:
            async with await session.get(url) as resp:
                result = await resp.text()

            # Retry PurpleAir download if dataset not downloaded, data string must
            # contain "created_at" column name to be considered valid
            retry_count = 0
            while "created_at" not in result and retry_count < 6:
                print(f"\nFailed to find data...retrying (attempt {retry_count}): {url}")
                async with await session.get(url) as resp:
                    result = await resp.text()
                retry_count += 1
            if retry_count >= 6:
                print("Unable to find data...skipping")
            elif retry_count > 0:
                print(f"\nSuccess!: {url}")

        return result

    @staticmethod
    def get_urls(urls):
        """
        Retrieves urls faster by making asynchronous requests (GET).

        Parameters
        ----------
        urls : list
            A list of urls (strings) to be accessed asynchronously.

        Returns
        -------
        responses : list
            A list of html responses (strings).

        """
        # Nest_asyncio is needed for running asyncio in an existing IPython event loop
        if NESTED:
            nest_asyncio.apply()
        loop = asyncio.get_event_loop()

        async def _get_url(urls):
            asyncio_tasks = []
            connector = aiohttp.TCPConnector(limit_per_host=MAX_CONNECTIONS)
            async with aiohttp.ClientSession(connector=connector) as session:
                for url in urls:
                    task = asyncio.create_task(AsyncRequest.__fetch_url(session, url))
                    asyncio_tasks.append(task)
                responses = await asyncio.gather(*asyncio_tasks)
            return responses

        print(f"Accessing {len(urls)} urls with async...", end="", flush=True)
        future = asyncio.ensure_future(_get_url(urls))
        responses = loop.run_until_complete(future)
        print("Done")
        return responses

    @staticmethod
    def post_url(url, forms):
        """
        Makes multiple POST requests to the provided url.

        Parameters
        ----------
        url : str
            Url that contains a form on its page.
        forms : list
            A list of dictionaries where each dictionary is a set of data values
            that gets POSTed to the website.

        Returns
        -------
        responses : list
            A list of the html responses (strings) for each form.

        """
        if NESTED:
            nest_asyncio.apply()
        loop = asyncio.get_event_loop()

        async def _post_url(url, forms):
            asyncio_tasks = []
            connector = aiohttp.TCPConnector(limit_per_host=MAX_CONNECTIONS)
            async with aiohttp.ClientSession(connector=connector) as session:
                for form in forms:
                    task = asyncio.create_task(AsyncRequest.__fetch_url(session, url, payload=form))
                    asyncio_tasks.append(task)
                responses = await asyncio.gather(*asyncio_tasks)
            return responses

        print(f"Posting {len(forms)} forms with async...", end="", flush=True)
        future = asyncio.ensure_future(_post_url(url, forms))
        responses = loop.run_until_complete(future)
        print("Done", flush=True)
        return responses


# class StandardRequest:
#     """A fallback class that can be utilized in the event the async version is
#     broken by unexpected deprecation"""

#     @staticmethod
#     def get_urls(urls):
#         responses = [requests.get(url) for url in urls]
#         responses = [r.text for r in responses if r.ok]
#         return responses

#     @staticmethod
#     def post_url(url, forms):
#         responses = [requests.post(url, data=form) for form in forms]
#         responses = [r.text for r in responses if r.ok]
#         return responses


# if __name__ == '__main__':
#     urls = ['https://example.com', 'https://google.com']
#     responses = AsyncRequest.get_urls(urls)
