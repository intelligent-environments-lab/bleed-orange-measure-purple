# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 23:29:10 2020

@author: CalvinL2
"""

from src.data.async_requests import(AsyncRequest, StandardRequest)


def test_async_requests():
    urls = ['https://google.com', 'https://youtube.com']
    resp = AsyncRequest.get_urls(urls)


def test_standard_requests():
    urls = ['https://google.com', 'https://youtube.com']
    resp = StandardRequest.get_urls(urls)


def test_tceq_post_async():
    url = 'https://www.tceq.texas.gov/cgi-bin/compliance/monops/yearly_summary.pl'
    request = {
        'submitted': '1',
        'select_site': 'site|||171',
        'user_year': '2020',
        'user_param': '88101',
        'time_format': '24hr',
        'report_format': 'comma',
    }
    resp = AsyncRequest.post_url(url, [request])
    assert 'Summary Report for 2020' in resp[0]


def test_tceq_post():
    url = 'https://www.tceq.texas.gov/cgi-bin/compliance/monops/yearly_summary.pl'
    request = {
        'submitted': '1',
        'select_site': 'site|||171',
        'user_year': '2020',
        'user_param': '88101',
        'time_format': '24hr',
        'report_format': 'comma',
    }
    resp = StandardRequest.post_url(url, [request])
    assert 'Summary Report for 2020' in resp[0]
