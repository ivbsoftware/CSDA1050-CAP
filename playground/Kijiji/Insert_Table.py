import psycopg2
import csv

try:
    connection = psycopg2.connect(user='postgres', password='csda1050',
                        host='/gcloudsql/river-howl-235515:us-east1:csda1050')
    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    print ( connection.get_dsn_parameters(),"\n")
    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")

    drop_table = '''Drop table gtarent_s;'''
    create_table_query = '''CREATE TABLE gtarent_s
          (AD_ID        INT,
          TITLE         TEXT,
          URL           TEXT,
          POSTDATE      Date, 
          LOCATION      TEXT,
          PRICE         TEXT); '''
    #show_table = '''SELECT * FROM pg_catalog.pg_tables;'''
    #test='''select * from information_schema.tables;'''
    cursor.execute(drop_table)
    connection.commit()
    cursor.execute(create_table_query)
   # mobile_records = cursor.fetchall()
    connection.commit()
    cursor.execute(show_table)
    query_result = cursor.fetchall()
    print("Print each row and it's columns values")
    for row in query_result:
       print("Name = ", row[0], )
       print(" = ", row[1])
       print("Price  = ", row[2], "\n")
    #print("Table created successfully in PostgreSQL ")

    with open('insert_rent_S.csv', newline='') as csvfile:
        csv_data = csv.reader(csvfile, delimiter=';')
        for row in csv_data:
            print(row)
            cursor.execute('INSERT INTO gtarent_s(AD_ID,TITLE,URL,POSTDATE, LOCATION,PRICE ) VALUES (%s, %s, %s, %s, %s, %s)', row)
    connection.commit()
    cursor.close()

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
