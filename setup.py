from setuptools import setup

long_desc='''
gw2apiwrapper is a Python library designed to abstract away the overhead/complexity of interacting with the official Guild Wars 2 (GW2) API.

The code written with it is meant to be easy to read and develop with minimal understanding of the actual GW2 API itself.
This is accomplished by abstracting out the standard JSON->dictionary scheme that is so commonly used and replace it with simple OOP-style notation.

See the URL below for more information, or call help() on any method provided by the library.
'''

setup(
    name='gw2apiwrapper',
    version='2.5.0b1',
    description='A simple wrapper around the offical Guild Wars 2 JSON API.',
    long_description=long_desc,
    url='https://github.com/PatchesPrime/gw2apiwrapper.git',
    author='R. "Patches" S.',
    author_email='patches@nullcorp.org',
    license='MIT',
    packages=['gw2apiwrapper'],
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Games/Entertainment',
    ],
    keywords='guild wars gw2 arenanet api wrapper',
    python_requires='>=3.5',
    zip_safe=False
)
