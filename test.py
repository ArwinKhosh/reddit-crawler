import sqlite3

connector = sqlite3.connect(":memory:")
cursor = connector.cursor()


dict_data = {
 'filename' : 'test.txt',
 'size' : '200'
}
table_name = 'test_table'
attrib_names = ", ".join(dict_data.keys())
attrib_values = ", ".join("?" * len(dict_data.keys()))
sql = f"INSERT INTO {table_name} ({attrib_names}) VALUES ({attrib_values})"
cursor.execute(sql, list(dict_data.values()))