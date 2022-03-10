from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable
from beautifultable import BeautifulTable
# from termcolor import colored

def colored(r,a):
    return r

def device_visualizer(app, deviceDrniId):
    print_summary(app, deviceDrniId)
    print_connections(app, deviceDrniId)
    print_ports(app, deviceDrniId)

def print_summary(app, deviceDrniId):
    print("\nSummary")
    with app.driver.session() as session:
            result = session.read_transaction(get_device_summary, deviceDrniId)
            row = result[0]
            table = BeautifulTable()
            table.columns.width = [25, 30]
            name = row.get("name", "") 
            status = row.get("status","") 
            type = row.get("type", "") 
            rack = "{0}: {1}".format(row.get("rackName", ""),row.get("rackPos", ""))
            table.rows.append(["Device Name",name])
            table.rows.append(["Device Type",type])
            table.rows.append(["Device status",status])
            table.rows.append(["Rack Positions",rack])
            
            table.columns.header.alignment= BeautifulTable.ALIGN_LEFT
            table.columns.alignment = BeautifulTable.ALIGN_LEFT
        
            print(table)

            
def print_ports(app, deviceDrniId):
    print("\nPorts_Informantion")
    with app.driver.session() as session:
            result = session.read_transaction(get_ports_info, deviceDrniId)
            table = BeautifulTable()
            table.columns.width = [5,20, 15, 10]
            table.columns.header=["#", "name","status","freeSpace"]
            index = 0
            for row in result:
                index = index+1
                name = row.get("name", "") 
                status = row.get("status","") 
                freeSpace = row.get("freeSpace", "") 
                if(freeSpace == 'G'):
                    table.rows.append([index, name,status,colored(freeSpace,"green")])
                else:
                    table.rows.append([index, name,status,freeSpace])
            
            table.columns.header.alignment= BeautifulTable.ALIGN_LEFT
            table.columns.alignment = BeautifulTable.ALIGN_LEFT
        
            print(table)


def print_connections(app, deviceDrniId):
    print("\nConnections")
    with app.driver.session() as session:
            result = session.read_transaction(get_device_connections, deviceDrniId)
            table = BeautifulTable()
            table.columns.width = [5,40, 15, 20]
            table.columns.header=["#", "name","status","type"]
            index = 0
            for row in result:
                index = index+1
                name = row.get("name", "") 
                status = row.get("status","") 
                type = row.get("type", "") 
                table.rows.append([index, name,status,type])
            
            table.columns.header.alignment= BeautifulTable.ALIGN_LEFT
            table.columns.alignment = BeautifulTable.ALIGN_LEFT
            print(table)

def get_device_connections(tx, deviceDrniId):
    query = (
            "MATCH (n:Device)<-[:HAS_CONNECTION_COMPONENT]-(c) "
            "where n.drniId = {0} "
            "RETURN distinct c.name as name,c.status as status,c.precomputedtypename as type"
        ).format(deviceDrniId)
    result = tx.run(query)
    return [row for row in result]

def get_device_summary(tx, deviceDrniId):
    query = (
            "MATCH (n:Device) "
            "where n.drniId = {0} "
            "RETURN n.deviceName as name, n.precomputedtypename as type,n.status as status,n.rackName as rackName, n.rackPositions as rackPos"
        ).format(deviceDrniId)
    result = tx.run(query)
    return [row for row in result]


def get_ports_info(tx, deviceDrniId):
    query = (
            "match (n:Device)-[:HAS*0..5]->(p:PhysicalPort) where n.drniId={0} return p.name as name,p.status as status,p.freeSpace as freeSpace"
        ).format(deviceDrniId)
    result = tx.run(query)
    return [row for row in result]
