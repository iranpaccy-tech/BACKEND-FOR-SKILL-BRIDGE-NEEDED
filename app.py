from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for, send_from_directory
import json
import os
from datetime import datetime
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch

app = Flask(__name__,
            template_folder='templates',
            static_folder='.',
            static_url_path='')
app.secret_key = 'skillbridge_secret_key_2026'

# Data storage files
DATA_DIR = 'data'
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
CERTIFICATES_FILE = os.path.join(DATA_DIR, 'certificates.json')
COURSES_FILE = os.path.join(DATA_DIR, 'courses.json')
JOBS_FILE = os.path.join(DATA_DIR, 'jobs.json')
GROUPS_FILE = os.path.join(DATA_DIR, 'groups.json')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

def load_data(filename, default=None):
    """Load data from JSON file"""
    if default is None:
        default = []
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return json.load(f)
        return default
    except:
        return default

def save_data(filename, data):
    """Save data to JSON file"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

# Initialize default data
def init_default_data():
    # Users
    if not os.path.exists(USERS_FILE):
        users = [
            {
                "id": 1,
                "firstName": "Demo",
                "lastName": "User",
                "email": "demo@skillbridge.com",
                "password": "password123",
                "role": "student",
                "createdAt": "2026-01-01T00:00:00Z"
            },
            {
                "id": 2,
                "firstName": "Admin",
                "lastName": "User",
                "email": "admin@skillbridge.com",
                "password": "admin123",
                "role": "admin",
                "createdAt": "2026-01-01T00:00:00Z"
            }
        ]
        save_data(USERS_FILE, users)

    # Certificates
    if not os.path.exists(CERTIFICATES_FILE):
        certificates = [
            {"id": 1, "title": 'JavaScript Fundamentals', "date": '2026-03-15', "credential": 'SB-JS-001', "userId": 1},
            {"id": 2, "title": 'Python Basics', "date": '2026-02-28', "credential": 'SB-PY-089', "userId": 1}
        ]
        save_data(CERTIFICATES_FILE, certificates)

    # Courses
    if not os.path.exists(COURSES_FILE):
        courses = [
            {"id": 1, "title": 'HTML & CSS Fundamentals', "instructor": 'Sarah Johnson', "duration": '4 weeks', "rating": 4.8, "students": 1250, "price": 49},
            {"id": 2, "title": 'JavaScript Mastery', "instructor": 'Michael Chen', "duration": '6 weeks', "rating": 4.9, "students": 890, "price": 79},
            {"id": 3, "title": 'React Development', "instructor": 'Priya Patel', "duration": '8 weeks', "rating": 4.7, "students": 756, "price": 99}
        ]
        save_data(COURSES_FILE, courses)

    # Jobs
    if not os.path.exists(JOBS_FILE):
        jobs = [
            {"id": 1, "title": 'Frontend Developer', "company": 'TechCorp', "location": 'Remote', "salary": '$70k-90k', "type": 'Full-time'},
            {"id": 2, "title": 'Full Stack Engineer', "company": 'StartupXYZ', "location": 'San Francisco', "salary": '$90k-120k', "type": 'Full-time'},
            {"id": 3, "title": 'UI/UX Designer', "company": 'DesignHub', "location": 'New York', "salary": '$60k-80k', "type": 'Contract'}
        ]
        save_data(JOBS_FILE, jobs)

    # Groups
    if not os.path.exists(GROUPS_FILE):
        groups = [
            {"id": 1, "name": 'JavaScript Masters', "description": 'Master advanced JavaScript concepts', "category": 'programming', "language": 'JavaScript', "members": 25, "maxMembers": 30},
            {"id": 2, "name": 'React Developers', "description": 'Build modern React applications', "category": 'framework', "language": 'JavaScript', "members": 18, "maxMembers": 25}
        ]
        save_data(GROUPS_FILE, groups)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    if session['user'].get('role') == 'admin':
        return redirect(url_for('admin'))
    return render_template('dashboard.html')

@app.route('/certificates')
def certificates():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('certificates.html')

@app.route('/login')
def login():
    if 'user' in session:
        if session['user'].get('role') == 'admin':
            return redirect(url_for('admin'))
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/courses')
def courses():
    return render_template('courses.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admin')
def admin():
    if 'user' not in session or session['user'].get('role') != 'admin':
        return redirect(url_for('login'))
    return render_template('admin.html')

# API Routes
@app.route('/api/auth/login', methods=['POST'])
def api_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    users = load_data(USERS_FILE)
    user = next((u for u in users if u['email'] == email and u['password'] == password), None)

    if user:
        user_data = {k: v for k, v in user.items() if k != 'password'}
        session['user'] = user_data
        return jsonify({"success": True, "user": user_data})
    else:
        return jsonify({"success": False, "message": "Invalid email or password"}), 401

@app.route('/api/auth/register', methods=['POST'])
def api_register():
    data = request.get_json()
    firstName = data.get('firstName')
    lastName = data.get('lastName', '')
    email = data.get('email')
    password = data.get('password')

    users = load_data(USERS_FILE)

    # Check if email already exists
    if any(u['email'] == email for u in users):
        return jsonify({"success": False, "message": "Email already registered"}), 400

    # Create new user
    new_user = {
        "id": max([u['id'] for u in users], default=0) + 1,
        "firstName": firstName,
        "lastName": lastName,
        "email": email,
        "password": password,
        "role": "student",
        "createdAt": datetime.now().isoformat()
    }

    users.append(new_user)
    save_data(USERS_FILE, users)

    user_data = {k: v for k, v in new_user.items() if k != 'password'}
    session['user'] = user_data

    return jsonify({"success": True, "user": user_data})

@app.route('/api/auth/status')
def auth_status():
    if 'user' in session:
        return jsonify({'logged_in': True, 'user': session['user']})
    return jsonify({'logged_in': False})

@app.route('/api/certificates', methods=['GET'])
def get_certificates():
    if 'user' not in session:
        return jsonify({"success": False, "message": "Not authenticated"}), 401

    user_id = session['user']['id']
    certificates = load_data(CERTIFICATES_FILE)
    user_certificates = [c for c in certificates if c.get('userId') == user_id]

    return jsonify({"success": True, "data": user_certificates})

@app.route('/api/certificates', methods=['POST'])
def add_certificate():
    if 'user' not in session:
        return jsonify({"success": False, "message": "Not authenticated"}), 401

    data = request.get_json()
    user_id = session['user']['id']

    certificates = load_data(CERTIFICATES_FILE)
    new_cert = {
        "id": max([c['id'] for c in certificates], default=0) + 1,
        "title": data['title'],
        "date": data['date'],
        "credential": data['credential'],
        "userId": user_id
    }

    certificates.append(new_cert)
    save_data(CERTIFICATES_FILE, certificates)

    return jsonify({"success": True, "certificate": new_cert})

@app.route('/api/certificates/<int:cert_id>', methods=['PUT'])
def update_certificate(cert_id):
    if 'user' not in session:
        return jsonify({"success": False, "message": "Not authenticated"}), 401

    data = request.get_json()
    user_id = session['user']['id']

    certificates = load_data(CERTIFICATES_FILE)
    cert = next((c for c in certificates if c['id'] == cert_id and c['userId'] == user_id), None)

    if not cert:
        return jsonify({"success": False, "message": "Certificate not found"}), 404

    cert.update({
        "title": data['title'],
        "date": data['date'],
        "credential": data['credential']
    })

    save_data(CERTIFICATES_FILE, certificates)
    return jsonify({"success": True, "certificate": cert})

@app.route('/api/certificates/<int:cert_id>', methods=['DELETE'])
def delete_certificate(cert_id):
    if 'user' not in session:
        return jsonify({"success": False, "message": "Not authenticated"}), 401

    user_id = session['user']['id']
    certificates = load_data(CERTIFICATES_FILE)
    certificates = [c for c in certificates if not (c['id'] == cert_id and c['userId'] == user_id)]

    save_data(CERTIFICATES_FILE, certificates)
    return jsonify({"success": True})

@app.route('/api/certificates/<int:cert_id>/download')
def download_certificate(cert_id):
    if 'user' not in session:
        return jsonify({"success": False, "message": "Not authenticated"}), 401

    user_id = session['user']['id']
    certificates = load_data(CERTIFICATES_FILE)
    cert = next((c for c in certificates if c['id'] == cert_id and c['userId'] == user_id), None)

    if not cert:
        return jsonify({"success": False, "message": "Certificate not found"}), 404

    # Create PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    story = []

    # Title
    title = Paragraph("SKILLBRIDGE ACADEMY", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))

    subtitle = Paragraph("Certificate of Completion", styles['Heading1'])
    story.append(subtitle)
    story.append(Spacer(1, 24))

    # Content
    content = f"""
    This is to certify that

    {session['user']['firstName']} {session['user'].get('lastName', '')}

    has successfully completed the course

    {cert['title']}

    Credential ID: {cert['credential']}
    Date Issued: {cert['date']}
    """

    cert_text = Paragraph(content, styles['Normal'])
    story.append(cert_text)

    doc.build(story)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"{cert['title'].replace(' ', '_')}_certificate.pdf",
        mimetype='application/pdf'
    )

@app.route('/api/courses')
def get_courses():
    courses = load_data(COURSES_FILE)
    return jsonify({"success": True, "data": courses})

@app.route('/api/jobs')
def get_jobs():
    jobs = load_data(JOBS_FILE)
    return jsonify({"success": True, "data": jobs})

@app.route('/api/groups')
def get_groups():
    groups = load_data(GROUPS_FILE)
    return jsonify({"success": True, "data": groups})

@app.route('/api/user')
def get_user():
    if 'user' in session:
        return jsonify({"success": True, "user": session['user']})
    return jsonify({"success": False, "message": "Not authenticated"}), 401

# Admin API routes
@app.route('/api/admin/users')
def admin_users():
    if 'user' not in session or session['user'].get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    users = load_data(USERS_FILE)
    return jsonify({'success': True, 'users': users})

@app.route('/api/admin/certificates')
def admin_certificates():
    if 'user' not in session or session['user'].get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    certificates = load_data(CERTIFICATES_FILE)
    return jsonify({'success': True, 'certificates': certificates})

@app.route('/api/admin/courses')
def admin_courses():
    if 'user' not in session or session['user'].get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    courses = load_data(COURSES_FILE)
    return jsonify({'success': True, 'courses': courses})

@app.route('/api/admin/jobs')
def admin_jobs():
    if 'user' not in session or session['user'].get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    jobs = load_data(JOBS_FILE)
    return jsonify({'success': True, 'jobs': jobs})

@app.route('/api/admin/groups')
def admin_groups():
    if 'user' not in session or session['user'].get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    groups = load_data(GROUPS_FILE)
    return jsonify({'success': True, 'groups': groups})

# Admin POST routes - Add new items
@app.route('/api/admin/users', methods=['POST'])
def admin_add_user():
    if 'user' not in session or session['user'].get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    users = load_data(USERS_FILE)
    
    new_user = {
        "id": max([u['id'] for u in users], default=0) + 1,
        "firstName": data.get('firstName', ''),
        "lastName": data.get('lastName', ''),
        "email": data.get('email', ''),
        "password": data.get('password', 'password123'),
        "role": data.get('role', 'student'),
        "createdAt": datetime.now().isoformat()
    }
    
    users.append(new_user)
    save_data(USERS_FILE, users)
    return jsonify({'success': True, 'user': new_user})

@app.route('/api/admin/certificates', methods=['POST'])
def admin_add_certificate():
    if 'user' not in session or session['user'].get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    certificates = load_data(CERTIFICATES_FILE)
    
    new_cert = {
        "id": max([c['id'] for c in certificates], default=0) + 1,
        "title": data.get('title', ''),
        "date": data.get('date', ''),
        "credential": data.get('credential', ''),
        "userId": int(data.get('userId', 1))
    }
    
    certificates.append(new_cert)
    save_data(CERTIFICATES_FILE, certificates)
    return jsonify({'success': True, 'certificate': new_cert})

@app.route('/api/admin/courses', methods=['POST'])
def admin_add_course():
    if 'user' not in session or session['user'].get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    courses = load_data(COURSES_FILE)
    
    new_course = {
        "id": max([c['id'] for c in courses], default=0) + 1,
        "title": data.get('title', ''),
        "instructor": data.get('instructor', ''),
        "duration": data.get('duration', ''),
        "rating": float(data.get('rating', 0)),
        "students": int(data.get('students', 0)),
        "price": int(data.get('price', 0))
    }
    
    courses.append(new_course)
    save_data(COURSES_FILE, courses)
    return jsonify({'success': True, 'course': new_course})

@app.route('/api/admin/jobs', methods=['POST'])
def admin_add_job():
    if 'user' not in session or session['user'].get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    jobs = load_data(JOBS_FILE)
    
    new_job = {
        "id": max([j['id'] for j in jobs], default=0) + 1,
        "title": data.get('title', ''),
        "company": data.get('company', ''),
        "location": data.get('location', ''),
        "salary": data.get('salary', ''),
        "type": data.get('type', '')
    }
    
    jobs.append(new_job)
    save_data(JOBS_FILE, jobs)
    return jsonify({'success': True, 'job': new_job})

@app.route('/api/admin/groups', methods=['POST'])
def admin_add_group():
    if 'user' not in session or session['user'].get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    groups = load_data(GROUPS_FILE)
    
    new_group = {
        "id": max([g['id'] for g in groups], default=0) + 1,
        "name": data.get('name', ''),
        "description": data.get('description', ''),
        "category": data.get('category', ''),
        "language": data.get('language', ''),
        "members": int(data.get('members', 0)),
        "maxMembers": int(data.get('maxMembers', 30))
    }
    
    groups.append(new_group)
    save_data(GROUPS_FILE, groups)
    return jsonify({'success': True, 'group': new_group})

# Admin PUT routes - Update items
@app.route('/api/admin/users/<int:user_id>', methods=['PUT'])
def admin_update_user(user_id):
    if 'user' not in session or session['user'].get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    users = load_data(USERS_FILE)
    user = next((u for u in users if u['id'] == user_id), None)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    user.update({
        "firstName": data.get('firstName', user.get('firstName')),
        "lastName": data.get('lastName', user.get('lastName')),
        "email": data.get('email', user.get('email')),
        "role": data.get('role', user.get('role'))
    })
    
    save_data(USERS_FILE, users)
    return jsonify({'success': True, 'user': user})

@app.route('/api/admin/certificates/<int:cert_id>', methods=['PUT'])
def admin_update_certificate(cert_id):
    if 'user' not in session or session['user'].get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    certificates = load_data(CERTIFICATES_FILE)
    cert = next((c for c in certificates if c['id'] == cert_id), None)
    
    if not cert:
        return jsonify({'error': 'Certificate not found'}), 404
    
    cert.update({
        "title": data.get('title', cert.get('title')),
        "date": data.get('date', cert.get('date')),
        "credential": data.get('credential', cert.get('credential')),
        "userId": int(data.get('userId', cert.get('userId')))
    })
    
    save_data(CERTIFICATES_FILE, certificates)
    return jsonify({'success': True, 'certificate': cert})

@app.route('/api/admin/courses/<int:course_id>', methods=['PUT'])
def admin_update_course(course_id):
    if 'user' not in session or session['user'].get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    courses = load_data(COURSES_FILE)
    course = next((c for c in courses if c['id'] == course_id), None)
    
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    
    course.update({
        "title": data.get('title', course.get('title')),
        "instructor": data.get('instructor', course.get('instructor')),
        "duration": data.get('duration', course.get('duration')),
        "rating": float(data.get('rating', course.get('rating', 0))),
        "students": int(data.get('students', course.get('students', 0))),
        "price": int(data.get('price', course.get('price', 0)))
    })
    
    save_data(COURSES_FILE, courses)
    return jsonify({'success': True, 'course': course})

@app.route('/api/admin/jobs/<int:job_id>', methods=['PUT'])
def admin_update_job(job_id):
    if 'user' not in session or session['user'].get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    jobs = load_data(JOBS_FILE)
    job = next((j for j in jobs if j['id'] == job_id), None)
    
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    job.update({
        "title": data.get('title', job.get('title')),
        "company": data.get('company', job.get('company')),
        "location": data.get('location', job.get('location')),
        "salary": data.get('salary', job.get('salary')),
        "type": data.get('type', job.get('type'))
    })
    
    save_data(JOBS_FILE, jobs)
    return jsonify({'success': True, 'job': job})

@app.route('/api/admin/groups/<int:group_id>', methods=['PUT'])
def admin_update_group(group_id):
    if 'user' not in session or session['user'].get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    groups = load_data(GROUPS_FILE)
    group = next((g for g in groups if g['id'] == group_id), None)
    
    if not group:
        return jsonify({'error': 'Group not found'}), 404
    
    group.update({
        "name": data.get('name', group.get('name')),
        "description": data.get('description', group.get('description')),
        "category": data.get('category', group.get('category')),
        "language": data.get('language', group.get('language')),
        "members": int(data.get('members', group.get('members', 0))),
        "maxMembers": int(data.get('maxMembers', group.get('maxMembers', 30)))
    })
    
    save_data(GROUPS_FILE, groups)
    return jsonify({'success': True, 'group': group})

# Admin DELETE routes
@app.route('/api/admin/users/<int:user_id>', methods=['DELETE'])
def admin_delete_user(user_id):
    if 'user' not in session or session['user'].get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    users = load_data(USERS_FILE)
    users = [u for u in users if u['id'] != user_id]
    save_data(USERS_FILE, users)
    return jsonify({'success': True})

@app.route('/api/admin/certificates/<int:cert_id>', methods=['DELETE'])
def admin_delete_certificate(cert_id):
    if 'user' not in session or session['user'].get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    certificates = load_data(CERTIFICATES_FILE)
    certificates = [c for c in certificates if c['id'] != cert_id]
    save_data(CERTIFICATES_FILE, certificates)
    return jsonify({'success': True})

@app.route('/api/admin/courses/<int:course_id>', methods=['DELETE'])
def admin_delete_course(course_id):
    if 'user' not in session or session['user'].get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    courses = load_data(COURSES_FILE)
    courses = [c for c in courses if c['id'] != course_id]
    save_data(COURSES_FILE, courses)
    return jsonify({'success': True})

@app.route('/api/admin/jobs/<int:job_id>', methods=['DELETE'])
def admin_delete_job(job_id):
    if 'user' not in session or session['user'].get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    jobs = load_data(JOBS_FILE)
    jobs = [j for j in jobs if j['id'] != job_id]
    save_data(JOBS_FILE, jobs)
    return jsonify({'success': True})

@app.route('/api/admin/groups/<int:group_id>', methods=['DELETE'])
def admin_delete_group(group_id):
    if 'user' not in session or session['user'].get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    groups = load_data(GROUPS_FILE)
    groups = [g for g in groups if g['id'] != group_id]
    save_data(GROUPS_FILE, groups)
    return jsonify({'success': True})

@app.route('/api/auth/logout', methods=['GET', 'POST'])
def api_logout():
    session.clear()
    if request.method == 'POST':
        return jsonify({'success': True})
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_default_data()
    app.run(debug=True, port=5000)