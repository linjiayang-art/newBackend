from flask import request, send_from_directory
from src import create_app
from src.core.auth import auth
app=create_app('development')


@app.route('/swagger-ui')
def swagger_ui():
    return send_from_directory('static', 'swagger-ui.html')

@app.route('/')
@auth.login_required
def index():
    return "Hello, {}!".format(auth.current_user())

@app.route('/admin')
@auth.login_required(role=['admin1', 'moderator'])
def admins_only():
    return "Hello {}, you are an admin or a moderator!".format(auth.current_user().password_hash)


if __name__ == '__main__':
    app.run(debug=True)