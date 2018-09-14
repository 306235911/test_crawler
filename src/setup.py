#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by weixiong
from setuptools import setup

setup(
    entry_points={
        'console_scripts': [
        ]
    },
    name='test_crawl',
    version='1.1.1',
    description='spider',
    url='https://github.com/306235911/test_crawler',
    author='pwx',
    author_email='306235911@qq.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.7'
    ],
    keywords='test common_crawler',
    packages=['common_crawler', 'common_crawler.tutorial.tutorial', 'dealer',
              'dealer.kafka', 'dealer.log', 'common_crawler.tutorial.tutorial.spiders']
)