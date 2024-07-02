from src.apis import api_v1

@api_v1.route('/')
def api_v1_index():
    return 'api_v1_index'