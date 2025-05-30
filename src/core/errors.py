from flask import abort, jsonify, render_template
from flask_wtf.csrf import CSRFError
from webargs.flaskparser import parser
from flask import jsonify
from marshmallow import ValidationError
from marshmallow import ValidationError
def register_errors(app):
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "code": 400,
            "msg": "Bad Request",
            "errors": error.description
        }), 400
        return render_template('errors/400.html', description=error.description), 400

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            "code": 404,
            "msg": "Page Not Found",
            "errors": error.description
        }), 404
        return render_template('errors/404.html', description=error.description), 404


    @app.errorhandler(500)
    def internal_server_error(error):
        print(error)
        
        return render_template('errors/500.html', description=error.description), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(error):
        return render_template('errors/400.html', description=error.description), 402
    
    @parser.error_handler
    def handle_webargs_error(err, req, schema, *, error_status_code, error_headers):
        # Raise an HTTP exception instead of returning a response
        abort(error_status_code or 400, description={
            "code": 400,
            "msg": "参数校验失败",
            "errors": err.messages
        })

