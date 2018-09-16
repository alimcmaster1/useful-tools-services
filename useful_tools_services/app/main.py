import json
import os
import re
from collections import Counter
from functools import wraps
from http import HTTPStatus

import cachetools.func as ct
import pandas as pd
from flask import Flask, request, Response
from flask_cors import CORS
from pymongo import MongoClient
from sklearn.feature_extraction.text import CountVectorizer

from useful_tools_services.app.connection import resourceItem, dbConnection

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})


def jsonify_response(func):
    @wraps(func)
    def jsonify():
        return Response(json.dumps(func()), mimetype='application/json')

    return jsonify


@app.route("/")
def hello():
    return "OK"


@app.route("/db/sites", methods=["GET"])
@jsonify_response
def get_all_webpage_urls():
    conn = dbConnection()
    site_urls = [row for row in conn.get_distinct_webpages()]
    return [row for row in site_urls]


@app.route("/db/links", methods=["GET"])
@jsonify_response
def get_all_items():
    conn = dbConnection()
    all_res = conn.select_all()
    dataset = [row.values() for row in all_res]

    df = pd.DataFrame(data=dataset, columns=all_res.keys())

    # Bucket by item group
    groups = []
    for group in df.item_group.unique():
        items = []
        for item in df.loc[df['item_group'] == group].values:
            items.append({"Group": item[0], "Name": item[1],
                          "Links": item[2], "Description": item[3]})
        groups.append({"Group": group, "Items": items})
    return {"Groups": groups}


@app.route("/db/links", methods=['POST'])
def insert_item() -> Response:
    try:
        resource = create_resource_item(request)
    except ValueError:
        return Response('Invalid Params', HTTPStatus.INTERNAL_SERVER_ERROR)

    conn = dbConnection()
    sql = conn.gen_insert_sql(resource)
    result_proxy = conn.execute_ins(sql)
    rows_inserted = result_proxy.rowcount
    result_proxy.close()
    return Response('Success {} rows INSERTED'.format(rows_inserted))


@app.route("/db/links", methods=["DELETE"])
def delete_item() -> Response:
    try:
        resource = create_resource_item(request)
    except ValueError:
        return Response('Invalid Params', HTTPStatus.INTERNAL_SERVER_ERROR)

    conn = dbConnection()
    sql = conn.gen_delete_sql(resource)
    result_proxy = conn.execute_ins(sql)
    rows_deleted = result_proxy.rowcount
    result_proxy.close()
    return Response('Success {} rows DELETED'.format(rows_deleted))


def create_resource_item(request: request) -> resourceItem:
    request_body = request.get_json()
    return resourceItem(request_body["group"],
                        request_body["item_name"],
                        request_body["links"],
                        request_body["resource_desc"])


@app.route("/mongo/tech_articles", methods=["GET"])
@jsonify_response
def mongo_tech_articles():
    count = pull_and_analyse_articles(os.getenv("MONGO_URL"))
    select_top_results = request.args.get('top')
    if select_top_results is not None:
        return dict(count.most_common(int(select_top_results)))

    return dict(count.items())


@ct.ttl_cache(maxsize=3, ttl=3600 * 3)
def pull_and_analyse_articles(mongo_url: str) -> Counter:
    # Pull this data into a cache on start up.
    client = MongoClient(mongo_url)
    coll = client[os.getenv("MONGO_DB")]["tech_articles"]
    return count_occurances(coll)


def count_occurances(coll):
    vectorizer = CountVectorizer(stop_words='english',
                                 max_features=100)
    count = Counter()
    for post in get_docs(coll):
        bag_words = vectorizer.fit_transform([post["document"]])
        for word, idx in vectorizer.vocabulary_.items():
            if re.search("(.*[a-z]){3}", word):
                count = count + Counter({word: int(bag_words[0, idx])})
    return count


def get_docs(coll):
    return coll.find()


if __name__ == '__main__':
    # Heroku defines the port we must use in the "PORT" env variable
    port = int(os.getenv("PORT", default=8000))
    print("Port to use {}".format(port))
    app.run(debug=True, host='0.0.0.0', port=port)
