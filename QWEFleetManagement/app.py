import hashlib
import bcrypt
from curses import flash
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
# Change this to a more secure key in production
app.secret_key = 'supersecretkey'

# Dummy data for demonstration purposes only
users = {'user1': 'password1', 'user2': 'password2'}
trucks = [
    {'id': '1', 'starting_location': 'Coventry',
        'destination': 'Manchester',  'security_team': 'Team 1', 'Progress': 'Out of Depot',
        'route': [
            {'location': 'Coventry', 'time': '13:00'},
            {'location': 'Birmingham', 'time': '14:30'},
            {'location': 'London', 'time': '17:00'},
            {'location': 'Manchester', 'time': '20:00'},
        ],
        'current_location': 'Coventry',
     },

    {'id': '2', 'starting_location': 'Coventry',
        'destination': 'Manchester',  'security_team': 'Team 2',
        'route': [
            {'location': 'Coventry', 'time': '13:00'},
            {'location': 'Birmingham', 'time': '14:30'},
            {'location': 'London', 'time': '17:00'},
            {'location': 'Manchester', 'time': '20:00'},
        ],
        'current_location': 'Coventry',

        'progress': 'on the way'

     },
]


@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Get the list of trucks
    truck_list = []
    for truck in trucks:
        # Check if the truck has a security team assigned
        if truck['security_team']:
            security_status = 'Assigned'
            security_action = 'Remove'
            security_url = url_for('remove_guard', truck_id=truck['id'])
        else:
            security_status = 'Unassigned'
            security_action = 'Assign'
            security_url = url_for(
                'assign_security_team', truck_id=truck['id'], index=trucks.index(truck))

        # progress as url to track progress
        progress_url = url_for('track_progress', index=trucks.index(truck))

        # Create a dictionary with the truck details and security status
        truck_dict = {'id': truck['id'], 'starting_location': truck['starting_location'],
                      'destination': truck['destination'], 'security_status': security_status,
                      'security_action': security_action, 'security_url': security_url,
                      'progress_url': url_for('track_progress', index=trucks.index(truck)),
                      'security_team': truck['security_team'],
                      'progress': progress_url,
                      'remove_route': url_for('remove_truck', index=trucks.index(truck)),
                      }
        truck_list.append(truck_dict)

    return render_template('dashboard.html', truck_list=truck_list)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username, password, users)
        if username not in users:
            return render_template('login.html', error='Invalid username or password')
        else:
            hashed_password = users[username]
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                session['username'] = username
                return redirect(url_for('index'))
            else:
                return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')


@ app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return render_template('signup.html', error='Username already taken')
        else:
            # Hash the password using bcrypt
            hashed_password = bcrypt.hashpw(
                password.encode('utf-8'), bcrypt.gensalt())
            users[username] = hashed_password
            return redirect(url_for('login'))
    else:
        return render_template('signup.html')


@ app.route('/add_truck', methods=['GET', 'POST'])
def add_truck():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        truck_id = request.form['truck_id']
        starting_location = request.form['starting_location']
        destination = request.form['destination']
        trucks.append({'id': truck_id, 'starting_location': starting_location,
                      'destination': destination, 'security_team': '',
                       'route': [
                           {'location': starting_location, 'time': '13:00'},
                           {'location': 'Birmingham', 'time': '14:30'},
                           {'location': 'London', 'time': '17:00'},
                           {'location': destination, 'time': '20:00'},
                       ],
                       'current_location': starting_location,
                       'progress': 'Out of Depot',


                       })
        return redirect(url_for('index'))
    else:
        return render_template('add_truck.html')


@ app.route('/remove_truck/<int:index>')
def remove_truck(index):
    if 'username' not in session:
        return redirect(url_for('login'))
    trucks.pop(index)
    return redirect(url_for('index'))


@ app.route('/assign_security_team/<int:index>', methods=['GET', 'POST'])
def assign_security_team(index):
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        security_team = request.form['security_team']
        trucks[index]['security_team'] = f'Team {security_team}'
        return redirect(url_for('index'))
    else:
        return render_template('assign_security_team.html', index=index, trucks=trucks)


@ app.route('/track_progress/<int:index>')
def track_progress(index):
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('track_progress.html', index=index, trucks=trucks)


@ app.route('/remove_guard/<truck_id>', methods=['GET'])
def remove_guard(truck_id):
    if 'username' not in session:
        return redirect(url_for('login'))
    # Find the truck with the given truck_id
    truck = next((t for t in trucks if t['id'] == truck_id), None)
    if not truck:
        flash(f"Truck with ID '{truck_id}' not found.", 'error')
        return redirect(url_for('index'))
    # Remove the security team from the truck
    truck['security_team'] = ''
    # flash('Security team removed from truck.', 'success')
    return redirect(url_for('index'))


@app.route('/remove-route/<int:truck_id>', methods=['POST'])
def remove_route(truck_id):
    trucks.pop(truck_id - 1)
    return redirect(url_for('index'))


@ app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

