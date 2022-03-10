from neo4j import GraphDatabase
from beautifultable import BeautifulTable

def nodeInfo(app, node_drni_id):
    print_info(app, node_drni_id)

def print_info(app, node_drni_id):
    with app.driver.session() as session:
            result = session.read_transaction(get_node_info, node_drni_id)
            row = result[0]
            table = BeautifulTable()
            table.columns.width = [25, 30, 25, 30]
           
            
            print("\nLabels = {0}".format(",".join(row.labels)))
            print("Properties :")
            a = 0
            list_to_append = []
            for x in row:
                if a < 2:
                    list_to_append.append(x)
                    list_to_append.append(row[x])
                    a = a + 1
                else:
                    table.rows.append(list_to_append)
                    list_to_append = []
                    list_to_append.append(x)
                    list_to_append.append(row[x])
                    a = 1
                
            
            table.columns.header.alignment= BeautifulTable.ALIGN_LEFT
            table.columns.alignment = BeautifulTable.ALIGN_LEFT
        
            print(table)


def get_node_info(tx, node_drni_id):
    query = (
            "MATCH (n) "
            "where n.drniId = {0} "
            "RETURN n"
        ).format(node_drni_id)
    result = tx.run(query)
    return [row['n'] for row in result]

