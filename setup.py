from setuptools import find_packages, setup
import os

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
long_description = open(os.path.join(ROOT_PATH, 'README.md')).read()

setup(name='fakeroute',
    version='0.1',
    description='',
    long_description=long_description,
    author='Paris-traceroute team',
    author_email='paris-traceroute@googlegroups.com',
    url='https://code.google.com/p/paris-traceroute/wiki/Fakeroute',
    packages=find_packages(),
    install_requires=[
        'dpkt',
        'python-nfqueue'
		#'NetfilterQueue'
    ],
    data_files = [
        ('/usr/share/fakeroute/targets', ['targets/127.1.1.1-asymlb', 'targets/127.1.1.2-lb', 'targets/127.1.1.3-double', 'targets/127.1.1.4-weird']),
    ],

)
