from flask import Flask
from routes.prompt_routes import prompt_bp


def create_app():

    app = Flask(__name__)

    app.register_blueprint(prompt_bp)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )