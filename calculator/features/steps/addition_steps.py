from behave import *

@step('I navigate to home page')
def step_impl(context):
    context.resp = context.client.get('/')

@then('Home Page should be displayed')
def step_impl(context):
    assert 'Home Page' in context.resp

@given(u'I have entered 50 as first number')
def step_impl(context):
    context.resp.form['first'] = '50'

@given(u'I have entered 70 as second number')
def step_impl(context):
    context.resp.form['second'] = '70'

@when(u'I press add')
def step_impl(context):
    context.resp = context.resp.form.submit()

@then(u'50 + 70 = 120 should be displayed')
def step_impl(context):
    assert '50 + 70 = 120' in context.resp