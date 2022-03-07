from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable
from beautifultable import BeautifulTable

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

    @staticmethod
    def _get_devices(tx):
        query = (
            "MATCH (n:Device) "
            "RETURN n limit 45"
        )
        result = tx.run(query)
        return [row["n"] for row in result]


if __name__ == "__main__":
    bolt_url = "bolt://localhost:7687"
    user = "neo4j"
    password = "drni"
    app = App(bolt_url, user, password)
    # app.create_friendship("Alice", "David")
    # app.find_person("Alice")
    app.get_devices()
    app.close()