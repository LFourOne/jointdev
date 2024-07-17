from app_flask.config.mysqlconnections import connectToMySQL
from app_flask import DATA_BASE

class Contact:
    def __init__(self, data):
        self.id = data.get('id')
        self.name = data.get('name')
        self.profile_picture = data.get('profile_picture')
        self.position = data.get('position')
        self.company = data.get('company')
        self.users_id1 = data.get('users_id1')
        self.users_id2 = data.get('users_id2')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
    
    @classmethod
    def add_contact(cls, data):
        query = """
                INSERT INTO contacts (users_id1, users_id2)
                VALUES (%(users_id1)s, %(users_id2)s)
                """
        return connectToMySQL(DATA_BASE).query_db(query, data)
    
    @classmethod
    def get_contacts(cls, users_id):
        query = """
                SELECT users.id, users.name, users.email, users.profile_picture, users.position, users.company
                FROM users
                JOIN contacts ON users.id = contacts.users_id2
                WHERE contacts.users_id1 = %(users_id)s;
                """
        results = connectToMySQL(DATA_BASE).query_db(query, {'users_id': users_id})
        contacts = []
        for result in results:
            contacts.append(cls(result))
        return contacts
    
    @classmethod
    def validate_contacts(cls, users_id):
        query = """
                SELECT users.id FROM users
                JOIN contacts ON users.id = contacts.users_id2
                WHERE contacts.users_id1 = %(users_id)s;
                """
        results = connectToMySQL(DATA_BASE).query_db(query, {'users_id': users_id})
        contacts = []
        for result in results:
            contacts.append(cls(result))
        return contacts