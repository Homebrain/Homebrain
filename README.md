# Homebrain

Control and monitor your home on your own terms.

[ ![Codeship Status for ErikBjare/Homebrain](https://codeship.com/projects/95112e30-60ec-0132-76d7-02eb9615503b/status?branch=master)](https://codeship.com/projects/51704)


## Usage

### Installation

Install dependencies with `python3 setup.py install`, if you are going to develop run `python3 setup.py develop` instead ([Why?](http://stackoverflow.com/questions/19048732/python-setup-py-develop-vs-install)).

### Running it

Run with `homebrain`


## Development

There is a [**Slack**](https://homebrain.slack.com/) for team communication and a [**Trello board**](https://trello.com/b/qTIPOiPS/homebrain) for planning.

### Documentation

There is currently no pre-built documentation, but you can easily build it yourself by installing sphinx and sphinx-autodoc-typehints:

    sudo pip3 install sphinx sphinx-autodoc-typehints

You can then build the docs by entering the `docs` folder and running:

    python3 -m sphinx -b html . _build

You will then find the built docs in `docs/_build/index.html`.

### Tests

The most convenient way to run the tests is with nose. Install with `pip3 install nose` and run with `nosetests` from the root directory of the project.

Tests are run automatically on Codeship (see the badge near the top of the README).
