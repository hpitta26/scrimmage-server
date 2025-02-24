from flask.cli import FlaskGroup
from scrimmage import app, db
import os

# Set Flask configuration using environment variables
os.environ['FLASK_RUN_HOST'] = '0.0.0.0'
os.environ['FLASK_RUN_PORT'] = '8000'
os.environ['FLASK_DEBUG'] = '1'  # Enable debug mode

# Create FlaskGroup instance
cli = FlaskGroup(app)

if __name__ == '__main__':
    cli()
