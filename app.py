from flask import request, send_from_directory
from src import create_app
from src.core.auth import auth
from src.models.system import UserInfo
app=create_app('development')


@app.route('/swagger-ui')
def swagger_ui():
    return send_from_directory('static', 'swagger-ui.html')

@app.route('/')
@auth.login_required
def index():
    return "Hello, {}!".format(auth.current_user())

@app.route('/admin')
@auth.login_required(role=['admin', 'moderator'])
def admins_only():
    user_info:UserInfo=auth.current_user()
    return "Hello {}, you are an admin or a moderator!".format(user_info.password_hash)




if __name__ == '__main__':
    app.run(debug=True)