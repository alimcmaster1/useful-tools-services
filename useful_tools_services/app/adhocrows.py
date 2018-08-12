from useful_tools_services.app.connection import dbConnection, resourceItem


class adhoc_data:
    ROWS = [
        ["Data manipulation in python", "Tom Augspurger",
         ["https://tomaugspurger.github.io",
          "https://www.youtube.com/watch?v=7vuO9QXDN50"],
         "Pandas Head to tail & blog "]]

    @staticmethod
    def adhoc_script_for_bulk_upload():
        conn = dbConnection()
        for item in adhoc_data.ROWS:
            ri = resourceItem(*item)
            sql = conn.gen_insert_sql(ri)
            conn.execute_ins(sql)
            print(sql)


adhoc_data.adhoc_script_for_bulk_upload()
