# 启动文件
from flask import Flask
from src import create_app
from src.models import create_tables

def main():
    app = create_app()

    with app.app_context():
        create_tables()

    app.run(debug=True, port=8080)

if __name__ == '__main__':
    main()