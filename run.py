from project import create_app, db
app = create_app()
app.app_context().push()
db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

# Remove debug=True line. Insecure.
# A Flask app appears to be run in debug mode. This may allow an attacker to run arbitrary code through the debugger.
# Running a Flask application with debug mode enabled may allow an attacker to gain access through the Werkzeug debugger.
