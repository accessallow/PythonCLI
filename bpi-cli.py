from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable
from beautifultable import BeautifulTable
from deviceVisualizer import device_visualizer

class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    
    def get_devices1(self):
        with self.driver.session() as session:
            result = session.read_transaction(self._get_devices)
            table = BeautifulTable()
            table.columns.width = [5,40, 10, 10, 20, 20, 50]
            table.columns.header=["#", "device_name","vendor","category","latest","drniId","description"]
            index = 0
            for row in result:
                index = index+1
                device_name = row._properties.get("name", "") 
                vendor = row._properties.get("vendor","") 
                cateogry = row._properties.get("category", "") 
                latest = row._properties.get("latest","") 
                drniId = row._properties.get("drniId", "") 
                description = row._properties.get("description", "") 
                # print("\nD : {device_name}".format(device_name=device_name))
                table.rows.append([index, device_name,vendor,cateogry,latest,drniId,description])
            
            table.columns.header.alignment= BeautifulTable.ALIGN_LEFT
            table.columns.alignment = BeautifulTable.ALIGN_LEFT
            print(table)


    def get_devices(self):
        with self.driver.session() as session:
            result = session.read_transaction(self._get_devices)
            output_list = self.result_to_list(result)
            list_count = len(output_list)
            if list_count<=20:
                self.print_list(output_list)
            else:
                print("Result set length : {0}".format(list_count))

                offset = 0
                while True:
                    i = input("Enter n records to display next 20 records, q to quit : ")
                    if i == 'q':
                        break
                    else:
                        sublist = output_list[offset : offset+20]
                        offset = offset+20
                        self.print_list(sublist)
                        if offset >= list_count:
                            break

    def print_list(self,list):
        table = BeautifulTable()
        table.columns.width = [5,40, 10, 10, 20, 20, 50]
        table.columns.header=["#", "device_name","vendor","category","latest","drniId","description"]
        index = 0
        for tup in list:
            index = tup[0]
            device_name = tup[1]
            vendor = tup[2]
            cateogry = tup[3] 
            latest = tup[4]
            drniId = tup[5]
            description = tup[6]
            table.rows.append([index, device_name,vendor,cateogry,latest,drniId,description])
        
        table.columns.header.alignment= BeautifulTable.ALIGN_LEFT
        table.columns.alignment = BeautifulTable.ALIGN_LEFT
        print(table)

    def result_to_list(self, result):
        output_list = []
        index = 0
        for row in result:
            index = index+1
            device_name = row._properties.get("name", "") 
            vendor = row._properties.get("vendor","") 
            cateogry = row._properties.get("category", "") 
            latest = row._properties.get("latest","") 
            drniId = row._properties.get("drniId", "") 
            description = row._properties.get("description", "")
            output_list.append((index,device_name,vendor,cateogry,latest,drniId,description))
        return output_list

    def get_metamodels(self):
        with self.driver.session() as session:
            result = session.read_transaction(self._get_metamodels)
            table = BeautifulTable()
            table.columns.width = [5,40, 15, 15, 15]
            table.columns.header=["#", "name","metamodel_id","latest","hypermodel_id"]
            index = 0
            for row in result:
                index = index+1
                device_name = row.get("name", "") 
                vendor = row.get("metamodel_id","") 
                cateogry = row.get("latest", "") 
                latest = row.get("hypermodel_id","") 
                
                table.rows.append([index, device_name,vendor,cateogry,latest])
            
            table.columns.header.alignment= BeautifulTable.ALIGN_LEFT
            table.columns.alignment = BeautifulTable.ALIGN_LEFT
            print(table)

    def get_folders(self, folder_name):
        with self.driver.session() as session:
            result = session.read_transaction(self._get_folder_list,folder_name)
            table = BeautifulTable()
            table.columns.width = [5,40, 15, 15, 15]
            table.columns.header=["#", "name","metamodel_id","latest","hypermodel_id"]
            index = 0
            for row in result:
                index = index+1
                device_name = row.get("name", "") 
                vendor = row.get("metamodel_id","") 
                cateogry = row.get("latest", "") 
                latest = row.get("hypermodel_id","") 
                
                table.rows.append([index, device_name,vendor,cateogry,latest])
            
            table.columns.header.alignment= BeautifulTable.ALIGN_LEFT
            table.columns.alignment = BeautifulTable.ALIGN_LEFT
            print(table)

    @staticmethod
    def _get_devices(tx):
        query = (
            "MATCH (n:Device) "
            "RETURN n limit 45"
        )
        result = tx.run(query)
        return [row["n"] for row in result]

    @staticmethod
    def _get_metamodels(tx):
        query = (
            "match (d:Metamodel) return distinct d.name as name,"
            " d.metamodelId as metamodel_id, d.latest as latest,d.hypermodelId as hypermodel_id order by d.name"
        )
        result = tx.run(query)
        return [row for row in result]
    
    @staticmethod
    def _get_folder_list(tx,folder_name):
        query = (
            "match (d:{0}) return distinct d.name as name,"
            " d.metamodelId as metamodel_id, d.latest as latest,d.hypermodelId as hypermodel_id order by d.name"
        ).format(folder_name)

        result = tx.run(query)
        return [row for row in result]


def cli_label(folder_stack):
    return "/".join(folder_stack)

if __name__ == "__main__":
    bolt_url = "bolt://localhost:7687"
    user = "neo4j"
    password = "drni"
    app = App(bolt_url, user, password)
    folder_stack = []

    while True:
        command = input("BPI-CLI/{0}>>".format(cli_label(folder_stack)))
        try:
            if command == "devices":
                app.get_devices()
            elif command == "metamodels":
                app.get_metamodels()
            elif command.startswith("cd "):
                if command == "cd ..":
                    if len(folder_stack)!=0:
                        folder_stack.pop()
                else:
                    folder = command.split(" ")[1]
                    print("Folder = {0}".format(folder))
                    folder_stack.append(folder)
            elif command == "ls":
                if len(folder_stack)>0:
                    present_folder = folder_stack[-1]
                    app.get_folders(present_folder)
                else:
                    app.get_metamodels()
            elif command == "test":
                device_visualizer(app,255859431696502445)
            elif command == "exit":
                break
            elif command == "q":
                break
        except Exception as e:
            print("Malformed DB Query")
            print(e)

    app.close()