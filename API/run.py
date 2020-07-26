from app import create_app
from my_settings import HOST

host = HOST['host']

if __name__ == '__main__':
    app = create_app()
    app.run(host=host, port=5000, debug=True)
