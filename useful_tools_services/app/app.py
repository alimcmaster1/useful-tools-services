import json
import os
from http import HTTPStatus

import pandas as pd
from flask import Flask, request, Response
from flask_cors import CORS

import connection as cn
from connection import resourceItem

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

@app.route("/")
def hello():
    return "OK"


@app.route("/db/links", methods=["GET"])
def get_all_items() -> Response:
    conn = cn.dbConnection()
    all_res = conn.select_all()
    dataset = [row.values() for row in all_res]

    df = pd.DataFrame(data=dataset, columns=all_res.keys())

    # Bucket by group server side so UI can avoid expensive data manipulation logic
    groups = []
    for group in df.item_group.unique():
        items = []
        for item in df.loc[df['item_group'] == group].values:
            items.append({"Group": item[0], "Name": item[1],
                          "Links": item[2], "Description": item[3]})
        groups.append({"Group": group, "Items": items})
    return json.dumps({"Groups": groups})


@app.route("/db/links", methods=['POST'])
def insert_item() -> Response:
    try:
        resource = create_resource_item(request)
    except ValueError:
        return Response('Invalid Params', HTTPStatus.INTERNAL_SERVER_ERROR)

    conn = cn.dbConnection()
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

    conn = cn.dbConnection()
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

if __name__ == '__main__':
    # Heroku defines the port we must use in the "PORT" env variable
    port = int(os.environ.get("PORT", 8000))
    print("Port to use {}".format(port))
    app.run(debug=True, host='0.0.0.0', port=port)
