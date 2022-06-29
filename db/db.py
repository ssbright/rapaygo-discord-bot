import psycopg2

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



