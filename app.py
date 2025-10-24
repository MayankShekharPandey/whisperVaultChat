from flask import Flask, render_template, request, redirect, url_for, session
import database

app = Flask(__name__)
app.secret_key = 'super_secret_key_123'

# Initialize database
with app.app_context():
    database.init_db()

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('chat'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('chat'))
        
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        
        if username and password:
            if database.verify_user(username, password):
                session['username'] = username
                return redirect(url_for('chat'))
            else:
                return render_template('login.html', error="Invalid username or password")
        else:
            return render_template('login.html', error="Please enter both username and password")
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('chat'))
        
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        confirm_password = request.form['confirm_password'].strip()
        
        if not username or not password:
            return render_template('register.html', error="Please fill in all fields")
        
        if password != confirm_password:
            return render_template('register.html', error="Passwords do not match")
        
        if len(username) < 3:
            return render_template('register.html', error="Username must be at least 3 characters")
        
        if len(password) < 4:
            return render_template('register.html', error="Password must be at least 4 characters")
        
        if database.register_user(username, password):
            session['username'] = username
            return redirect(url_for('chat'))
        else:
            return render_template('register.html', error="Username already exists")
    
    return render_template('register.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        message = request.form['message'].strip()
        if message and len(message) > 0:
            database.add_message(session['username'], message)
        return redirect(url_for('chat'))
    
    messages = database.get_messages()
    return render_template('chat.html', messages=messages, username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)