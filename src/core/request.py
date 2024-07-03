from flask_sqlalchemy.record_queries import get_recorded_queries


def register_request_handlers(app):
    @app.after_request
    def query_profiler(response):
        app.logger.info('Recorded queries: %d', len(get_recorded_queries()))
        for q in get_recorded_queries():
            if q.duration >= app.config['BACKEND_SLOW_QUERY_THRESHOLD']:
                app.logger.warning(
                    'Slow query: Duration: '
                    f'{q.duration:f}s\nQuery: {q.statement}\n  parameters: {q. parameters}\n'
                )
        return response