import os
from app import create_app

# create the app from the env vars
config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)

# run it
if __name__ == '__main__':
    app.run()