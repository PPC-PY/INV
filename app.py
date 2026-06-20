from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL Database Configuration
db_config = {
    'host': 'mysql-2c08e112-nifsppc2024-80e8.i.aivencloud.com',
    'port': 12823, # Notice we added the port here because it's not the default 3306!
    'user': 'avnadmin',
    'password': 'AVNS_QUPIQMLjGC62nlL1vHD', # Put the password you just found
    'database': 'defaultdb'
}

@app.route('/')
def index():
    message = request.args.get('message', '')
    inventory_items = []
    
    try:
        # Connect to MySQL and fetch all rows from the Inventory table
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True) # returns data as dictionaries
        
        cursor.execute("SELECT Part_No, Part_Name, Qty FROM Inventory")
        inventory_items = cursor.fetchall()
        
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        message = f"Database Error: {err}"
        
    return render_template('index.html', message=message, inventory=inventory_items)

@app.route('/add_item', methods=['POST'])
def add_item():
    if request.method == 'POST':
        part_no = request.form['part_no']
        part_name = request.form['part_name']
        qty = request.form['qty']
        
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            
            sql_query = "INSERT INTO Inventory (Part_No, Part_Name, Qty) VALUES (%s, %s, %s)"
            values = (part_no, part_name, qty)
            
            cursor.execute(sql_query, values)
            conn.commit()
            
            cursor.close()
            conn.close()
            return redirect(url_for('index', message="Data Inserted Successfully!"))
            
        except mysql.connector.Error as err:
            return f"Database Error: {err}"

if __name__ == '__main__':
    app.run(debug=True)
