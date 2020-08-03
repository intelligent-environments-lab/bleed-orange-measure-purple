# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import aiohttp
import asyncio
import nest_asyncio

import requests


class AsyncRequest:
    @staticmethod
    async def __fetch_url(session, url, payload=None):
        ''' This method is intended to be called by get_urls(urls) or post_url()'''

        # print('One')
        if payload is not None:
            # print('Posting')
            async with await session.post(url, data=payload) as resp:
                result = await resp.text()
        else:
            # print('Getting')
            async with await session.get(url) as resp:
                result = await resp.text()

        # print('Two')
        return result

    @staticmethod
    def get_urls(urls):
        '''
        Retrieves urls faster by making asynchronous requests (GET).

        Parameters
        ----------
        urls : list
            A list of urls (strings) to be accessed asynchronously.

        Returns
        -------
        responses : list
            A list of html responses (strings).

        '''
        # Nest_asyncio is needed for running asyncio in an existing IPython event loop
        nest_asyncio.apply()
        loop = asyncio.get_event_loop()

        async def _get_url(urls):
            asyncio_tasks = []
            async with aiohttp.ClientSession() as session:
                for url in urls:
                    task = asyncio.create_task(AsyncRequest.__fetch_url(session, url))
                    asyncio_tasks.append(task)
                responses = await asyncio.gather(*asyncio_tasks)
            return responses

        print(f'Accessing {len(urls)} urls with async...', end='')
        future = asyncio.ensure_future(_get_url(urls))
        responses = loop.run_until_complete(future)
        print('Done')
        return responses

    @staticmethod
    def post_url(url, forms):
        '''
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

        '''
        nest_asyncio.apply()
        loop = asyncio.get_event_loop()

        async def _post_url(url, forms):
            asyncio_tasks = []
            async with aiohttp.ClientSession() as session:
                for form in forms:
                    task = asyncio.create_task(
                        AsyncRequest.__fetch_url(session, url, payload=form)
                    )
                    asyncio_tasks.append(task)
                responses = await asyncio.gather(*asyncio_tasks)
            return responses

        print(f'Posting {len(forms)} forms with async...', end='')
        future = asyncio.ensure_future(_post_url(url, forms))
        responses = loop.run_until_complete(future)
        print('Done')
        return responses


class StandardRequest:
    """ A fallback class that can be utilized in the event the async version is
    broken by unexpected deprecation"""

    @staticmethod
    def get_urls(urls):
        responses = [requests.get(url) for url in urls]
        responses = [r.text for r in responses if r.ok]
        return responses

    @staticmethod
    def post_url(url, forms):
        responses = [requests.post(url, data=form) for form in forms]
        responses = [r.text for r in responses if r.ok]
        return responses


if __name__ == '__main__':
    urls = ['https://example.com', 'https://google.com']
    responses = AsyncRequest.get_urls(urls)
