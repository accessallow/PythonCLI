from neo4j import GraphDatabase
from beautifultable import BeautifulTable
import json
import pyjsonviewer
import tempfile
import os

def nodeJson(app, node_drni_id):
    print_info(app, node_drni_id)

def print_info(app, node_drni_id):
    with app.driver.session() as session:
            result = session.read_transaction(get_node_info, node_drni_id)
            row = result[0]
            y = json.dumps(row._properties)
            with open("./json_file.json","w") as f:
                f.write(y)
            pyjsonviewer.view_data(json_file="./json_file.json")
            os.remove("./json_file.json")


def get_node_info(tx, node_drni_id):
    query = (
            "MATCH (n) "
            "where n.drniId = {0} "
            "RETURN n"
        ).format(node_drni_id)
    result = tx.run(query)
    return [row['n'] for row in result]

