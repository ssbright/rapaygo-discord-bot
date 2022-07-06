import psycopg2
import sys
sys.path.append('./')
from api_handler import  payment_confirmed_checker

from variables import *


global conn
global cur

def persist_invoice(invoice_id,payment_hash,recipient,sender,action,amount):
    sql = f'''
    INSERT into invoice_audit (invoice_id, payment_hash, sender, recipient, action, amount, status)
    VALUES ('{invoice_id}','{payment_hash}','{sender}','{recipient}','{action}',{amount},'PENDING')
    
    '''
    conn = psycopg2.connect("dbname='rapaygo_invoice' user='sydney'")
    #conn = None
    #try:
    #    conn = psycopg2.connect("dbname='rapaygo_invoice' user='postgres'")
    #except:
    #    print("I am unable to connect to the database.")

    cur = conn.cursor()

    cur.execute(sql)
    conn.commit()
    conn.close()

def fetch_all_invoice():

    #cur.execute("""select id from invoice_audit where status= 'PENDING'""")
    cur.execute("""select * from invoice_audit""")
    query_results = cur.fetchall()
    print(query_results)
    print(query_results[1][4])
    for row in query_results:
        payHash =row[4]
        if payment_confirmed_checker(payHash) == "COMPLETED":
            cur.execute("""update audit_invoice set status='COMPLETED'""")



