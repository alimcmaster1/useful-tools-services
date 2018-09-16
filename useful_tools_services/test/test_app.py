import json
import os

from pymongo import MongoClient

from useful_tools_services.app import main
from useful_tools_services.app.main import count_occurances


def datapath(path: str) -> str:
    """Get the path to a data file.

    Parameters
    ----------
    path : str
        Path to the file, relative to `useful_tools_services/tests/`

    Returns
    -------
    path : path including `useful_tools_services/tests/`.
    """
    BASE_PATH = os.path.dirname(__file__)
    return "{}/{}".format(BASE_PATH, path)


def test_word_frequency_aggregation(monkeypatch):
    def mockreturn(collection):
        with open(datapath('data/sample-doc.json'), 'r') as myfile:
            return [json.loads(myfile.read())]

    monkeypatch.setattr(main, 'get_docs', mockreturn)

    testClient = MongoClient()
    test_collection = testClient["test_database"]["test_collection"]

    occurances = count_occurances(test_collection)

    # Check 5 most common occurances are as expected
    expected = [
        ("deep", 12),
        ("book", 9),
        ("learning", 8),
        ("press", 5),
        ("mit", 4)
    ]
    assert occurances.most_common(5) == expected
