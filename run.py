from flaskServer import app

if __name__ == "__main__":
    host = app.config.get('HOST')
    port = app.config.get('PORT')
    app.run(host=host,port=port)