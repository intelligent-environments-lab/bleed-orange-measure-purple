# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import aiohttp
import asyncio
import nest_asyncio

import requests


class AsyncRequest():
    @staticmethod
    async def __fetch_url(session, url, payload=None):
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
        nest_asyncio.apply()
        loop = asyncio.get_event_loop()

        async def _post_url(url, forms):
            asyncio_tasks=[]
            async with aiohttp.ClientSession() as session:
                    for form in forms:
                        task = asyncio.create_task(AsyncRequest.__fetch_url(session, url, payload=form))
                        asyncio_tasks.append(task)
                    responses = await asyncio.gather(*asyncio_tasks)
            return responses

        print(f'Posting {len(forms)} forms with async...', end='')
        future = asyncio.ensure_future(_post_url(url, forms))
        responses = loop.run_until_complete(future)
        print('Done')
        return responses

class StandardRequest:
    """ Use this class only if the AsyncRequest one isn't working"""
    @staticmethod
    def get_urls(urls):
        responses = [requests.get(url)for url in urls]
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
