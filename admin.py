from config import Config
from create_app import init_app
from admin import blueprints

app = init_app(blueprints)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=Config.admin_port, debug=True)
