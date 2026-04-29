from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import sys
import os
from pathlib import Path

# Add data directory to path
sys.path.insert(0, str(Path(__file__).parent / "data"))

from User.SDB_User import check_user_credentials, create_table as create_user_table
from Horses.SDB import (
    create_table as create_horse_table,
    add_horse,
    get_all_horses,
    get_horse,
    update_horse,
    update_distance,
    delete_horse
)
from Horses.Horse import Horse

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your-secret-key-change-this'


@app.before_request
def initialize_databases():
    """Create tables on first request."""
    create_user_table()


def require_login(f):
    """Decorator to check if user is logged in."""
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Not authenticated.'}), 401
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function


@app.route('/')
def index():
    """Serve the start screen."""
    return render_template('index.html')


@app.route('/login.html')
def login_page():
    """Serve the login page."""
    return render_template('login.html')


@app.route('/api/login', methods=['POST'])
def api_login():
    """Validate credentials and return user info."""
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return jsonify({'success': False, 'message': 'Please fill in both fields.'}), 400

    user = check_user_credentials(username, password)

    if user:
        session['user_id'] = user.id_user
        session['username'] = user.username
        session['role'] = user.role.name
        
        # Create user-specific horse database
        create_horse_table(user.id_user)
        
        return jsonify({
            'success': True,
            'message': f'Welcome, {user.username}!',
            'user_id': user.id_user,
            'username': user.username,
            'role': user.role.name
        }), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid username or password.'}), 401


@app.route('/main.html')
def main_page():
    """Serve the main page."""
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    
    return render_template('main.html')


@app.route('/api/horses', methods=['GET'])
@require_login
def api_get_all_horses():
    """Get all horses for the current user."""
    try:
        user_id = session.get('user_id')
        role = session.get('role')
        horses = get_all_horses(user_role=role, user_id=user_id)
        
        import math
        horse_list = []
        for horse_id, name, distance, time, theta_deg in horses:
            speed = 0 if time == 0 else (distance / time) * math.sin(math.radians(theta_deg))
            horse_list.append({
                'id': horse_id,
                'name': name,
                'distance': distance,
                'time': time,
                'theta': theta_deg,
                'speed': round(speed, 2)
            })
        
        return jsonify({'success': True, 'horses': horse_list}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/horses', methods=['POST'])
@require_login
def api_add_horse():
    """Add a new horse."""
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        time = int(data.get('time', 0))
        theta = int(data.get('theta', 0))
        
        if not name or time <= 0:
            return jsonify({'success': False, 'message': 'Invalid horse data.'}), 400
        
        user_id = session.get('user_id')
        role = session.get('role')
        
        horse = Horse(name, time, theta)
        add_horse(horse, user_role=role, user_id=user_id)
        
        return jsonify({'success': True, 'message': 'Horse added successfully.'}), 201
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/horses/<int:horse_id>', methods=['GET'])
@require_login
def api_get_horse(horse_id):
    """Get a specific horse."""
    try:
        user_id = session.get('user_id')
        role = session.get('role')
        horse = get_horse(horse_id, user_role=role, user_id=user_id)
        
        if not horse:
            return jsonify({'success': False, 'message': 'Horse not found.'}), 404
        
        import math
        horse_id, name, distance, time, theta_deg = horse
        speed = 0 if time == 0 else (distance / time) * math.sin(math.radians(theta_deg))
        
        return jsonify({
            'success': True,
            'horse': {
                'id': horse_id,
                'name': name,
                'distance': distance,
                'time': time,
                'theta': theta_deg,
                'speed': round(speed, 2)
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/horses/<int:horse_id>', methods=['PUT'])
@require_login
def api_update_horse(horse_id):
    """Update a horse."""
    try:
        data = request.get_json()
        name = data.get('name', '').strip() or None
        time = data.get('time')
        theta = data.get('theta')
        
        if time is not None:
            time = int(time)
        if theta is not None:
            theta = int(theta)
        
        user_id = session.get('user_id')
        role = session.get('role')
        
        update_horse(horse_id, new_name=name, new_time=time, new_theta_deg=theta, user_role=role, user_id=user_id)
        
        return jsonify({'success': True, 'message': 'Horse updated successfully.'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/horses/<int:horse_id>/distance', methods=['PUT'])
@require_login
def api_update_distance(horse_id):
    """Update horse distance."""
    try:
        data = request.get_json()
        distance = int(data.get('distance', 0))
        
        if distance <= 0:
            return jsonify({'success': False, 'message': 'Invalid distance.'}), 400
        
        user_id = session.get('user_id')
        role = session.get('role')
        
        update_distance(horse_id, distance, user_role=role, user_id=user_id)
        
        return jsonify({'success': True, 'message': 'Distance updated successfully.'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/horses/<int:horse_id>', methods=['DELETE'])
@require_login
def api_delete_horse(horse_id):
    """Delete a horse."""
    try:
        user_id = session.get('user_id')
        role = session.get('role')
        
        delete_horse(horse_id, user_role=role, user_id=user_id)
        
        return jsonify({'success': True, 'message': 'Horse deleted successfully.'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/logout', methods=['POST'])
def logout():
    """Logout the current user."""
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully.'}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
