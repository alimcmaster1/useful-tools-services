import json
import os
from http import HTTPStatus

import connection as cn
import pandas as pd
from flask import Flask, request, Response

from useful_tools_services.app.connection import linksTable
from useful_tools_services.app.connection import resourceItem

app = Flask(__name__)


@app.route("/")
def hello():
    return "OK"


@app.route("/db/links", methods=["GET"])
def get_all_items() -> Response:
    conn = cn.dbConnection()
    all_res = conn.select_all()
    columns = linksTable.useful_links.c
    dataset = [[row[columns.item_group], row[columns.item_name],
                row[columns.links], row[columns.resource_description]]
               for row in all_res]
    df = pd.DataFrame(data=dataset, columns=all_res.keys())

    # Bucket by group server side so UI can avoid expensive data manipulation logic
    groups = []
    for group in df.item_group.unique():
        items = []
        for item in df.loc[df['item_group'] == group].values:
            items.append({"Group": item[0], "Name": item[1],
                          "Link": item[2], "Description": item[3]})
        groups.append({"Group": group, "Items": items})
    return json.dumps({"Groups": groups})


@app.route("/db/links", methods=['PUT'])
def insert_item() -> Response:
    try:
        resource = get_resource_item(request)
    except ValueError:
        return Response('Invalid Params', HTTPStatus.INTERNAL_SERVER_ERROR)

    conn = cn.dbConnection()
    sql = conn.gen_insert_sql(resource)
    result_proxy = conn.execute_ins(sql)
    result_proxy.close()
    return Response('OK')


@app.route("/db/links", methods=["DELETE"])
def delete_item() -> Response:
    try:
        resource = get_resource_item(request)
    except ValueError:
        return Response('Invalid Params', HTTPStatus.INTERNAL_SERVER_ERROR)

    conn = cn.dbConnection()
    sql = conn.gen_delete_sql(resource)
    result_proxy = conn.execute_ins(sql)
    result_proxy.close()
    return Response('OK')


def get_resource_item(request) -> resourceItem:
    group = request.args.get('group')
    item_name = request.args.get('name')
    links = request.args.get('links')
    resource_desc = request.args.get('resource_desc')

    return resourceItem(group, item_name, links, resource_desc)


if __name__ == '__main__':
    # Heroku defines the port we must use in the "PORT" env variable
    port = int(os.environ.get("PORT", 8000))
    print("Port to use {}".format(port))
    app.run(debug=True, host='0.0.0.0', port=port)
