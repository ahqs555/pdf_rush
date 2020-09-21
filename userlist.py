from werkzeug.security import generate_password_hash
# ...
USERS = [
    {
        "id": 1,
        "name": 'TestUser1',
        "password": generate_password_hash('123')
    },
    {
        "id": 2,
        "name": 'lily',
        "password": generate_password_hash('123')
    },
    {
        "id": 3,
        "name": 'tom',
        "password": generate_password_hash('123')
    }
]