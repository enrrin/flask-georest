from dotenv import load_dotenv
import os

# pip install python-dotenv
load_dotenv()


class Config(object):
    DEBUG = False
    TESTING = False
    # SQLAlchemy
    uri_template = 'postgresql://{user}:{pw}@{url}/{db}'
    SQLALCHEMY_DATABASE_URI = uri_template.format(
        user=os.environ.get("POSTGRES_USER"),
        pw=os.environ.get("POSTGRES_PASSWORD"),
        url=os.environ.get("POSTGRES_URL"),
        db=os.environ.get("POSTGRES_DB"))
    # Silence the deprecation warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # API settings
    API_PAGINATION_PER_PAGE = 10


class DevelopmentConfig(Config):
    DEBUG = True


class TestConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    # production config
    pass


def get_config(env=None):
    if env is None:
        try:
            env = "ENV"
        except Exception:
            env = 'development'
            print('env is not set, using env:', env)

    if env == 'production':
        return ProductionConfig()
    elif env == 'test':
        return TestConfig()

    return DevelopmentConfig()
