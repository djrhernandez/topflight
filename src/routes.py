from ariadne import graphql_sync
from ariadne.explorer import ExplorerGraphiQL
from flask import jsonify, request

def init_app(app, schema, client, db):
    @app.route('/')
    def health_check():
        return "OK :)"


    @app.route("/graphql", methods=["GET"])
    def graphql_explorer():
        return ExplorerGraphiQL().html(None), 200


    @app.route("/graphql", methods=["POST"])
    def graphql_server():
        data = request.get_json()
        success, result = graphql_sync(
            schema,
            data,
            context_value=request,
            debug=app.debug
        )
        status_code = 200 if success else 400
        return jsonify(result), status_code
    
    
    @app.route("/winston", methods=["GET"])
    def find_winston():
        data = request.get_json()
        
        status_code = 200 if data else 400
        return jsonify(data), status_code