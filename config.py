import os

from dotenv import load_dotenv


def is_development():
    return os.getenv('ENVIRONMENT') == 'development'


if is_development():
    load_dotenv()
    print('Application is running in dev mode')

else:
    print('Application is running in prod mode')
        
SENTRY_DSN = os.getenv('SENTRY_DSN')