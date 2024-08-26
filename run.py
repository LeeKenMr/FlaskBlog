from app import app #app目录下的__init__.py中的app对象

if __name__ == '__main__':

    app.run(port=80,debug=True)