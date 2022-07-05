import psycopg2
import sys
sys.path.append('./')
from api_handler import bot_commands, payment_confirmed_checker
from time import sleep

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
    conn = psycopg2.connect("dbname='rapaygo_invoice' user='sydney'")
    cur = conn.cursor()
    #cur.execute("""select id from invoice_audit where status= 'PENDING'""")
    cur.execute("""select * from invoice_audit""")
    query_results = cur.fetchall()
    print(query_results)
    print(query_results[1][4])
    for row in query_results:
        payHash =row[4]
        if payment_confirmed_checker(payHash) == "COMPLETED":
            cur.execute("""update audit_invoice set status='COMPLETED'""")
def update_db():
    conn = psycopg2.connect("dbname='rapaygo_invoice' user='sydney'")
    cur = conn.cursor()
    #cur.execute("""select id from invoice_audit where status= 'PENDING'""")
    cur.execute("""select * from invoice_audit""")
    query_results = cur.fetchall()
    for row in query_results:
        sleep(5)
        print(f"inspect row {row}")
        payHash =row[4]
        curr_status = row[9]
        print(curr_status)
        print(payHash)
        if (payment_confirmed_checker(payHash) == "COMPLETED") and (curr_status != "COMPLETED"):
            cur.execute(f"""update invoice_audit set status='COMPLETED' where payment_hash='{payHash}'""")
            print("payment confirmation updated")

def test_update():
    conn = psycopg2.connect("dbname='rapaygo_invoice' user='sydney'")
    cur = conn.cursor()
    #cur.execute("""select id from invoice_audit where status= 'PENDING'""")
    cur.execute("""select * from invoice_audit""")
    query_results = cur.fetchall()

    cur.execute(f"""update invoice_audit set status='COMPLETED' where payment_hash='67ceb89e9c8aad3bd54500d06f19e30cc2ce79513fb1ff41dbf28188669aecc4'""")
    print("payment confirmation updated")

test_update()