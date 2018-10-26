from setuptools import setup

setup(
    name='tweetdigger',
    url='https://github.com/luizzan/tweetdigger',
    author='Luiz Zanini',
    author_email='tweetdigger@luizzanini.com',
    packages=['tweetdigger'],
    version='0.1.9',
    install_requires = [
    	'beautifulsoup4',
        'requests',
        'lxml',
    ],
)
