# 启动文件
from flask import Flask
from src import create_app

def main():
    app = create_app()

    if __name__ == '__main__':
        app.run(debug = True)

if __name__ == '__main__':
    main()