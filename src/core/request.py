from flask import jsonify
from flask_sqlalchemy.record_queries import get_recorded_queries
from marshmallow import ValidationError
from webargs.flaskparser import parser

def register_request_handlers(app):
    @app.after_request
    def query_profiler(response):
        # app.logger.info('Recorded queries: %d', len(get_recorded_queries()))
        for q in get_recorded_queries():
            if q.duration >= app.config['BACKEND_SLOW_QUERY_THRESHOLD']:
                app.logger.warning(
                    'Slow query: Duration: '
                    f'{q.duration:f}s\nQuery: {q.statement}\n  parameters: {q. parameters}\n'
                )
        return response
'''
    @parser.error_handler(ValidationError)
    def handle_webargs_error(err, req, schema, *, error_status_code, error_headers):
        """统一处理 webargs 参数校验失败"""
        response = jsonify({
            "code": 400,
            "msg": "参数错误",
            "errors": err.messages  # e.g. {"email": ["Missing data for required field."]}
        })
        response.status_code = error_status_code or 400
        return response'''