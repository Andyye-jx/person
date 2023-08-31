from config import Config
from create_app import init_app
from app import blueprints

app = init_app(blueprints)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.app_port)
