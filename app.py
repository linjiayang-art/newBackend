from flask import send_from_directory
from src import create_app

app=create_app('development')


@app.route('/swagger-ui')
def swagger_ui():
    return send_from_directory('static', 'swagger-ui.html')


if __name__ == '__main__':

    app.run(debug=True)