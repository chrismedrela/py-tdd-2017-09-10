from webtest import TestApp
from webapp import app

def before_scenario(context, scenario):
    context.client = TestApp(app)
