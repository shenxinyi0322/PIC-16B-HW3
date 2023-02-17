from flask import Flask
from flask import render_template, request, g
import sqlite3

app=Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def submit():
    if request.method == 'GET' :
        return render_template("submit.html")
    else:
        insert_message(request)
        return render_template("submit.html", done = True)

#Function that create the database of messages
def get_message_db():
    #Check whether there is a database called message_db in the g attribute of the app
    #if so, return such database
    try:
        return g.message_db
    
    #if not,connect to database message_db 
    except:
        g.message_db = sqlite3.connect("messages_db.sqlite")
        
        #if there is no table called messages exists in message_db, create it with three
        #columns: id column (integer), handle column (text), and message column (text)
        cursor = g.message_db.cursor()
        cmd = """
        CREATE TABLE IF NOT EXISTS messages (
        id INT, 
        handle TEXT, 
        message TEXT)
        """
        cursor.execute(cmd)
        return g.message_db

#Function that insert a user message into the database of messages  
def insert_message(request):
    #Extract the message and the handle from request
    message=request.form["message"]
    handle=request.form["handle"]
    
    #Get a cursor in the message database
    db = get_message_db()
    cursor = db.cursor()
    
    #Count the number of rows in the message database
    cursor.execute("SELECT COUNT(*) FROM messages")
    rows = cursor.fetchone()[0] + 1
    
    #Insert new message into the table
    cursor.execute('INSERT INTO messages (id, handle, message) VALUES (?, ?, ?)',(rows, handle, message))
    
    #Comit changes & Close Connection
    db.commit()
    db.close()

def random_messages(n):
    #Get a cursor in the message database
    db = get_message_db()
    cursor = db.cursor()
    
    #Randomly select messages and collect all of their information
    cursor.execute('SELECT * FROM messages ORDER BY RANDOM() LIMIT ?', (n,))
    messages=cursor.fetchall()
    
    #Close Connection
    db.close()
    return messages


@app.route("/view/")
def view():
    #Randomly show 5 messages
    messages = random_messages(5)
    return render_template("view.html", messages=messages)