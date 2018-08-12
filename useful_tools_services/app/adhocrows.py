from useful_tools_services.app.connection import dbConnection, resourceItem


class adhoc_data:
    ROWS = [
        ["Data manipulation in python", "Tom Augspurger",
         ["https://tomaugspurger.github.io",
          "https://www.youtube.com/watch?v=7vuO9QXDN50"],
         "Pandas Head to tail & blog "],

        ["Data manipulation in python", "Numba",
         ["https://numba.pydata.org"],
         "Support compilation of Python on run on CPU/GPU"],

        ["Data manipulation in python",
         "Natural Language Processing Google Cloud",
         [
             ("https://googlecloudplatform.github.io/"
              "google-cloud-python/latest/language/usage.html")],
         ("Google Natural Language API and other"
          "Google Cloud Client Libraries in python")],

        ["Data manipulation in python", "Logistic Regression/TFIDF Kaggle.",
         [
             ("https://www.kaggle.com/sudhirnl7/"
              "logistic-regression-tfidf/notebook")],
         "Pandas Head to tail & blog"],

        ["Machine Learning", "Pytorch",
         ["https://pytorch.org"],
         "Deep learning framework- Tensor computation and DNNs"],

        ["Machine Learning", "Deep Learning Guide",
         ["http://www.deeplearningbook.org"],
         "Pandas Head to tail & blog"],

        ["Other", "Crypto- Truffle Framework",
         ["https://truffleframework.com"],
         "Development framework for Ethereum"],

        ["Other", "Flink DataStream API",
         ["http://training.data-artisans.com/dataStream/basics.html"],
         "Guide to the flink datasteam api"],

        ["Other", "Rest API Aut",
         ["https://vertx.io/blog/writing-secure-vert-x-web-apps"],
         "Guide to rest API Auth in Vertx"],

    ]

    @staticmethod
    def adhoc_script_for_bulk_upload():
        conn = dbConnection()
        for item in adhoc_data.ROWS:
            ri = resourceItem(*item)
            sql = conn.gen_insert_sql(ri)
            conn.execute_ins(sql)
            print(sql)


adhoc_data.adhoc_script_for_bulk_upload()
