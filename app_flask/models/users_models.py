from app_flask.config.mysqlconnections import connectToMySQL
from flask import flash
from app_flask import DATA_BASE, EMAIL_REGEX

class User:
    def __init__(self, data):
        self.id = data.get('id')
        self.qr = data.get('qr')
        self.name = data.get('name')
        self.email = data.get('email')
        self.password = data.get('password')
        self.profile_picture = data.get('profile_picture')
        self.position = data.get('position')
        self.company = data.get('company')
        self.description = data.get('description')
        self.phone_number = data.get('phone_number')
        self.web = data.get('web')
        self.linkedin = data.get('linkedin')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
        self.has_visited = data.get('has_visited')
    
    @classmethod
    def create_one(cls, data):
        query = """
                INSERT INTO users(name, email, password)
                VALUE (%(name)s, %(email)s, %(password)s);
                """
        return connectToMySQL(DATA_BASE).query_db(query, data)
    
    @classmethod
    def update_qr(cls, data):
        query = """
                UPDATE users
                set qr = %(qr_path)s
                WHERE id = %(user_id)s
                """
        return connectToMySQL(DATA_BASE).query_db(query, data)

    @classmethod
    def obtain_one(cls, data):
        query = """
                SELECT *
                FROM users
                WHERE email = %(email)s;
                """
        result = connectToMySQL(DATA_BASE).query_db(query, data)
        if len(result) == 0:
            return None
        return cls(result[0])
    @classmethod
    def obtain_one_profile(cls, data):
        query = """
                SELECT id, name, email, profile_picture, position, company, description, phone_number, web, linkedin, created_at, updated_at
                FROM users
                WHERE id = %(id)s
                """
        result = connectToMySQL(DATA_BASE).query_db(query, data)
        if len(result) == 0:
            return None
        return cls(result[0])

    @classmethod
    def obtain_all(cls, current_user_id):
        query = """
                SELECT id, name, email, profile_picture, position, company, description, phone_number, web, linkedin, created_at, updated_at
                FROM users
                WHERE id != %(current_user_id)s
                """
        results = connectToMySQL(DATA_BASE).query_db(query, {'current_user_id': current_user_id})
        return [cls(result) for result in results]
    
    @classmethod
    def update_profile(cls, data):
        query = """
                UPDATE users
                SET name = %(name)s, email = %(email)s, profile_picture = %(profile_picture)s, position = %(position)s, company = %(company)s, description = %(description)s, phone_number = %(phone_number)s, web = %(web)s, linkedin = %(linkedin)s
                WHERE id = %(id)s
                """
        return connectToMySQL(DATA_BASE).query_db(query, data)

    @classmethod
    def validate_email(cls, email):
        query = """
                SELECT email from users
                WHERE email = %(email)s
                """
        result = connectToMySQL(DATA_BASE).query_db(query, {'email': email})
        return len(result) > 0
    
    @classmethod
    def validate_email_edit(cls, email, user_id):
        query = """
                SELECT email FROM users
                WHERE email = %(email)s AND id != %(user_id)s
                """
        result = connectToMySQL(DATA_BASE).query_db(query, {'email': email, 'user_id': user_id})
        return len(result) > 0
    
    @classmethod
    def user_has_visited(cls, user_id):
        query = """
                UPDATE users
                SET has_visited = 1
                WHERE id = %(user_id)s
                """
        return connectToMySQL(DATA_BASE).query_db(query, {'user_id': user_id})
    
    @staticmethod
    def validate_register(data):

        is_valid = True

        if len(data['name']) < 3:
            is_valid = False
            flash('Nombre inválido', 'name_error')
        
        if len(data['password']) < 7:
            is_valid = False
            flash('La contraseña debe tener mínimo 7 carácteres', 'password_error')

        if data['password'] != data['password_confirm']:
            is_valid = False
            flash('Las contraseñas no coinciden', 'password_confirm_error')

        if not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash('El correo electrónico no es correcto', 'email_error')
        
        return is_valid
    
    @staticmethod
    def validate_edit_profile(data):

        is_valid = True

        if len(data['name']) < 5:
            is_valid = False
            flash('Nombre inválido', 'name_error')

        if len(data['name']) > 21:
            is_valid = False
            flash('El nombre debe tener menos caracteres', 'name_error')

        if len(data['position']) < 4:
            is_valid = False
            flash('Tu puesto debe tener al menos 4 caracteres', 'position_error')
            
        if len(data['position']) < 4:
            is_valid = False
            flash('Tu puesto debe tener al menos 4 caracteres', 'position_error')

        if len(data['company']) < 3:
            is_valid = False
            flash('El nombre de la empresa debe tener al menos 3 caracteres', 'company_error')

        if len(data['description']) > 246:
            is_valid = False
            flash('La descripción debe tener menos de 256 caracteres', 'description_error')
        
        if len(data['phone_number']) > 15 or len(data['phone_number']) <= 14:
            is_valid = False
            flash('Ingrese un número válido', 'phone_number_error')
        
        if not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash('El correo electrónico no es correcto', 'email_error')
        
        return is_valid