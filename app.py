from src import create_app

app=create_app('development')

app.run(debug=True)