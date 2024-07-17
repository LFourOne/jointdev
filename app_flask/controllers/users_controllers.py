from flask import render_template, request, redirect, session
from app_flask.models.users_models import User
from app_flask.models.contacts_models import Contact
from app_flask import app, IMAGE_FOLDER
from flask import flash
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import os
from PIL import Image
import qrcode
import uuid

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/success', methods=['POST'])
def login_success():

    user_login = User.obtain_one(request.form)

    if user_login == None:
        flash('Los datos ingresados no son correctos', 'login_password_error')
        return redirect('/login')

    if not bcrypt.check_password_hash(user_login.password, request.form['password']):
        flash('Los datos ingresados no son correctos', 'login_password_error')
        return redirect("/login")

    else:

        if session:
            session.clear()

        session['id'] = user_login.id
        
        user_id = session['id']
        qr_path = generate_qr(user_id)

        data = {
            'user_id' : session['id'],
            'qr_path' : qr_path
        }

        User.update_qr(data)

        session['qr'] = qr_path

        session['name'] = user_login.name
        session['email'] = user_login.email
        session['profile_picture'] = user_login.profile_picture
        session['position'] = user_login.position
        session['company'] = user_login.company
        session['description'] = user_login.description
        session['phone_number'] = user_login.phone_number
        session['web'] = user_login.web
        session['linkedin'] = user_login.linkedin
        session['has_visited'] = user_login.has_visited

    return redirect('/welcome')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register/process', methods=['POST'])
def register_process():
    
    email = request.form['email']

    if User.validate_register(request.form) == False:
        return redirect('/register')

    elif User.validate_email(email):
        flash('El correo electrónico ya está en uso.', 'email_error')
        return redirect('/register')

    else:

        encrypted_password = bcrypt.generate_password_hash(request.form['password'])

        data = {
        **request.form,
        'password' : encrypted_password
        }

        User.create_one(data)
        
        return redirect('/login')

@app.route('/welcome')
def welcome():
    if 'id' not in session:
        return redirect('/login')
    
    elif session['has_visited'] == True:
        return redirect('/home')

    else:
        return render_template('welcome.html')
    
@app.route('/welcome/edit/profile')
def welcome_edit_profile():
    if 'id' not in session:
        return redirect('/login')
    
    elif session['has_visited'] == True:
        return redirect('/home')
    
    else:
        return render_template('welcome_edit.html')
    
@app.route('/welcome/edit/profile/process', methods=['POST'])
def welcome_process():
    if 'id' not in session:
        return redirect('/login')
    
    user_id = session['id']
    new_email = request.form.get('email')
    
    if User.validate_edit_profile(request.form) == False:
        return redirect('/welcome/edit/profile')

    elif User.validate_email_edit(new_email, user_id):
        flash('El correo electrónico ya está en uso.', 'email_error')
        return redirect('/welcome/edit/profile')

    else:

        new_image = request.files['file']

        if new_image and allowed_file(new_image.filename):
            file_name = secure_filename(new_image.filename)
            new_image.save(os.path.join(IMAGE_FOLDER, file_name))

        else:
            if 'profile_picture' in session and session['profile_picture']:
                file_name = session['profile_picture'].split('/')[-1]
            else:
                file_name = 'picture.svg'


        data = {
            'id': session.get('id'),
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'profile_picture': f'/img/profile_pics/{file_name}',
            'position' : request.form.get('position'),
            'company' : request.form.get('company'),
            'description': request.form.get('description'),
            'web': request.form.get('web'),
            'phone_number': request.form.get('phone_number'),
            'linkedin' : request.form.get('linkedin')
        }

        User.update_profile(data)

        session.update(data)

        session['name'] = data['name']
        session['email'] = data['email']
        session['profile_picture'] = data['profile_picture']
        session['position'] = data['position']
        session['company'] = data['company']
        session['description'] = data['description']
        session['web'] = data['web']
        session['phone_number'] = data['phone_number']
        session['linkedin'] = data['linkedin']

        User.user_has_visited(user_id)
        session['has_visited'] = True

        return redirect('/home')

@app.route('/home')
def home():
    if 'id' not in session:
        return redirect('/login')
    else:
        return render_template('home.html')

@app.route('/search')
def search():
    if 'id' not in session:
        return redirect('/login')
    else:
        current_user_id = session['id']

        users = User.obtain_all(current_user_id)

        contacts = Contact.validate_contacts(current_user_id)

        contacts_ids = {contact.id for contact in contacts}

        num_contacts = len(contacts_ids)

        return render_template('search.html', users=users, contacts_ids=contacts_ids, num_contacts=num_contacts)
    
@app.route('/profile')
def profile():
    if 'id' not in session:
        return redirect('/login')
    else:
        return render_template('profile.html')

@app.route('/profile/edit')
def edit_profile():
    if 'id' not in session:
        return redirect('/login')
    else:
        return render_template('edit_profile.html')

def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/profile/edit/process', methods=['POST'])
def edit_profile_process():

    if 'id' not in session:
        return redirect('/login')
    
    
    user_id = session['id']
    new_email = request.form.get('email')

    if User.validate_edit_profile(request.form) == False:
        return redirect('/profile/edit')

    elif User.validate_email_edit(new_email, user_id):
        flash('El correo electrónico ya está en uso.', 'email_error')
        return redirect('/profile/edit')

    else:

        new_image = request.files['file']

        if new_image and allowed_file(new_image.filename):
            file_name = secure_filename(new_image.filename)
            new_image.save(os.path.join(IMAGE_FOLDER, file_name))

        else:
            if 'profile_picture' in session and session['profile_picture']:
                file_name = session['profile_picture'].split('/')[-1]
            else:
                file_name = 'picture.svg'

        data = {
            'id': session.get('id'),
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'profile_picture': f'/img/profile_pics/{file_name}',
            'position' : request.form.get('position'),
            'company' : request.form.get('company'),
            'description': request.form.get('description'),
            'web': request.form.get('web'),
            'phone_number': request.form.get('phone_number'),
            'linkedin' : request.form.get('linkedin')
        }

        session.update(data)

        User.update_profile(data)

        session['name'] = data['name']
        session['email'] = data['email']
        session['profile_picture'] = data['profile_picture']
        session['position'] = data['position']
        session['company'] = data['company']
        session['description'] = data['description']
        session['web'] = data['web']
        session['phone_number'] = data['phone_number']
        session['linkedin'] = data['linkedin']

        return redirect('/profile')


@app.route('/profile/user/<user_id>')
def profiles_user(user_id):
    if 'id' not in session:
        return redirect('/login')
    
    else:

        user = User.obtain_one_profile({'id': user_id})
        
        return render_template('profile_user.html', user=user)
    
@app.route('/add-contact/<user_id>', methods=['POST'])
def add_contact(user_id):
    if 'id' not in session:
        return redirect('/login')
    
    else:

        users_id = session['id']

        data = {
            'users_id1' : users_id,
            'users_id2' : user_id
        }

        Contact.add_contact(data)

    return redirect('/search')

@app.route('/contacts')
def contacts():
    if 'id' not in session:
        return redirect('/login')
    else:
        
        users_id = session['id']

        contacts = Contact.get_contacts(users_id)

        print(contacts)

        return render_template('contacts.html', contacts=contacts)


@app.route('/share/qr')
def share_qr():
    if 'id' not in session:
        return redirect('/login')
    else:
        return render_template('share_qr.html')
    
@app.route('/scan/qr')
def scan_qr():
    if 'id' not in session:
        return redirect('/login')
    else:
        return render_template('scan_qr.html')

def generate_qr(user_id):
    base_url = '/add-contact/'
    unique_id = uuid.uuid4()
    data = f'{base_url}{user_id}?uid={unique_id}'

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white').convert('RGB')
    img = img.resize((275, 275), Image.LANCZOS)

    qr_folder = 'app_flask/static/img/qr'
    os.makedirs(qr_folder, exist_ok=True)

    file_path = os.path.join(qr_folder, f'qruser_{user_id}.png')
    img.save(file_path)

    # Retornar la ruta relativa
    return f'/static/img/qr/qruser_{user_id}.png'