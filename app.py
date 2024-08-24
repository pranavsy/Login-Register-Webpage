from flask import Flask, render_template, request, redirect, url_for,flash
import csv
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'af0c9e18ea50c81da4b772be9bd19e28b5f08e528a33f654'

def write_to_csv(data):
    csv_path = os.path.join(os.getcwd(), 'userinfo.csv')
    with open(csv_path, mode='a', newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(data.values())

def read_csv():
    csv_path = os.path.join(os.getcwd(), 'userinfo.csv')
    users = []
    with open(csv_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            users.append({'username': row[1], 'password': row[5]})
    return users

def check_credentials(username, password):
    users = read_csv()
    for user in users:
        if user['username'] == username and user['password'] == password:
            return True
    return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    full_name = request.form['full_name']
    username = request.form['username']
    department = request.form['department']
    year = request.form['year']
    section = request.form['section']
    password = request.form['password']
    confirm_password = request.form['confirm_password']


    if not all([full_name, username, department, year, section, password, confirm_password]):
        flash("All fields are required.", 'error')
        return render_template('index.html')

    if password != confirm_password:
        flash("Passwords do not match.", 'error')
        return render_template('index.html')

    write_to_csv({
        'full_name': full_name,
        'username': username,
        'department': department,
        'year': year,
        'section': section,
        'password': password
    })

    flash("Registration successful!", 'success')
    return render_template('index.html', full_name='', username='', department='', year='', section='')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']

    # Check credentials
    if check_credentials(username, password):
        # Redirect to a different website after successful login
        return redirect("http://192.168.10.17:5500/index.html")
    else:
        return "Invalid credentials. Please try again."

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')



