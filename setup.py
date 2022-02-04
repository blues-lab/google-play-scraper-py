import os
from setuptools import setup, find_packages

# The directory containing this file.
WORK_DIR = os.path.dirname(os.path.abspath(__file__))

# The text of the README file.
README = os.path.join(WORK_DIR, 'README.md')
with open(README, 'r') as f:
    long_description = f.read()

setup(
    name='google-play-scraper-py',
    version='0.2.4',
    description='Scrape application data from the Google Play store.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/blues-lab/google-play-scraper-py',
    author='Berkeley Lab for Usable and Experimental Security (BLUES)',
    author_email='blues@berkeley.edu',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9'
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'scraper=scraper.__main__:main',
        ]
    },
)
