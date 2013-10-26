import os

# application related configurations
APPLICATION_NAME = "Know-Your-Government"

# production/development related configurations
PRODUCTION = os.environ.get('SERVER_SOFTWARE', '').startswith('Google App Engine')
DEVELOPMENT = not PRODUCTION
DEBUG = DEVELOPMENT