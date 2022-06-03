
from beautifultable import BeautifulTable
from termcolor import colored

def connection_info(app, deviceDrniId):
    print_components(app, deviceDrniId)
    

def print_components(app, deviceDrniId):
    print("\nConnection Components")
    with app.driver.session() as session:
            result = session.read_transaction(get_components, deviceDrniId)
            table = BeautifulTable()
            table.columns.width = [5,30, 20,20,20, 10, 15, 10, 10, 10]
            table.columns.header=["#", "Name","drniId","metamodelId","Type","End","Not Route","Section","Segment","Sequence"]
            index = 0
            for row in result:
                index = index+1
                name = row.get("name", "") 
                drniId = row.get("drniId", "")
                metamodelId = row.get("mmId", "") 
                type = row.get("type","") 
                Eoc = row.get("Eoc", "") 
                nr = row.get("nr", "") 
                secNo = row.get("secNo", "") 
                segNo = row.get("segNo", "") 
                seq = row.get("seq", "") 
                table.rows.append([index, name, drniId, metamodelId, type, Eoc, nr, secNo, segNo, seq])
            
            table.columns.header.alignment= BeautifulTable.ALIGN_LEFT
            table.columns.alignment = BeautifulTable.ALIGN_LEFT
        
            print(table)

def get_components(tx, deviceDrniId):
    query = (
            "MATCH (c)-[r:HAS_CONNECTION_COMPONENT]->(p)"
            "where c.drniId = {0} "
            "RETURN p.name as name,p.drniId as drniId, p.metamodelId as mmId, p.precomputedtypename as type,r.isEndOfConnection as Eoc,r.isNotInRoute as nr,r.sectionNumber as secNo,r.segmentNumber as segNo,r.seq as seq"
        ).format(deviceDrniId)
    result = tx.run(query)
    return [row for row in result]

