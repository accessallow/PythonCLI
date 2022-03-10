from beautifultable import BeautifulTable

def network_info(app, network_drni_id):
    rels = type_of_rels(app,network_drni_id)
    for r in rels:
        print("Node(s) with Reletionship : {0}".format(r))
        print_connnected_table(app, network_drni_id,r)


def type_of_rels(app, network_drni_id):
    print("\nReletionships with this Network:")
    rellist = []
    with app.driver.session() as session:
            result = session.read_transaction(_type_of_rels, network_drni_id)
            table = BeautifulTable()
            table.columns.width = [5,40, 15]
            table.columns.header=["#", "type","count"]
            index = 0
            for row in result:
                index = index+1
                reltype = row.get("reltype", "")
                if reltype in ['CREATE','MODIFY']:
                    continue
                count = row.get("count","") 
                table.rows.append([index, reltype, count])
                rellist.append(reltype)
            
            table.columns.header.alignment= BeautifulTable.ALIGN_LEFT
            table.columns.alignment = BeautifulTable.ALIGN_LEFT
            print(table)
    return rellist

def _type_of_rels(tx, network_drni_id):
    query = (
            "match (n:Network)-[r]-(m) where n.drniId = {0} return distinct TYPE(r) as reltype, count(r) as count"
        ).format(network_drni_id)
    result = tx.run(query)
    return [row for row in result]


def print_connnected_table(app, network_drni_id, rel_name):
    with app.driver.session() as session:
            result = session.read_transaction(_rel_items, network_drni_id,rel_name)
            table = BeautifulTable()
            table.columns.width = [5,15,30,10,15,30,25,15]
            table.columns.header=["#", "rel_latest","name","metamodel_id", "drniId","labels","latest","status"]
            index = 0
            for row in result:
                index = index+1
                list_row = [index]
                for r in row:
                    list_row.append(r)
                table.rows.append(list_row)               
            
            table.columns.header.alignment= BeautifulTable.ALIGN_LEFT
            table.columns.alignment = BeautifulTable.ALIGN_LEFT
            print(table)

def _rel_items(tx, network_drni_id,rel_name):
    query = (
            "match (n:Network)-[r:{0}]-(m) where n.drniId = {1} "
            "return r.latest, m.name,m.metamodelId,m.drniId, labels(m) as labels, m.latest, m.status"
        ).format(rel_name,network_drni_id)
    result = tx.run(query)
    return [row for row in result]