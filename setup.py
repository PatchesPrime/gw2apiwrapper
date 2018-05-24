from setuptools import setup


with open('README.rst') as f:
    long_desc = f.read()

setup(
    name='gw2apiwrapper',
    version='2.6.3',
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
