from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='homebrain',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/development.html#single-sourcing-the-version
    version='0.1.0',

    description='',
    long_description='',

    # The project's main homepage.
    url='https://github.com/ErikBjare/homebrain',

    # Author details
    author='Homebrain contributors',
    author_email='',

    # Choose your license
    license='',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Pick your license as you wish (should match "license" above)
        #'License :: OSI Approved :: MIT License',

        # Indicate who your project is intended for
        # 'Intended Audience :: Developers',  # " ".join(["developers"] * 2**8))
        # 'Intended Audience :: System Administrators',
        # 'Intended Audience :: End Users/Desktop',

        # 'Topic :: System :: Monitoring',
        # 'Topic :: System :: Logging',
        # 'Topic :: Utilities',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',

        'Operating System :: POSIX :: Linux',
        # 'Operating System :: MacOS :: MacOS X',
        # 'Operating System :: Microsoft :: Windows',

        # 'Environment :: X11 Applications',
        # 'Environment :: MacOS X',
        # 'Environment :: Win32 (MS Windows)',
    ],

    # What does your project relate to?
    keywords='iot internet_of_things',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=["tests"]),

    # Required to bundle the web resources
    include_package_data=True,
    package_data={'': ['*.html', '*.js', '*.css']},
    zip_safe=False,

    # List run-time dependencies here.  These will be installed by pip when your
    # project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/technical.html#install-requires-vs-requirements-files
    install_requires=['flask', 'requests', 'mypy-lang', 'websocket-server', 'websocket-client',
                      'netifaces', 'netifaces'], # Useful hopefuls: tzlocal, pymongo

    entry_points={
        'console_scripts': ['homebrain = homebrain:start']
    }
)
