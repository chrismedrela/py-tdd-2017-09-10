from behave import *

@step(u'I navigate to Home Page')
def step_impl(ctx):
    ctx.resp = ctx.client.get('/')

@given(u'I enter {value} as {field}')
def step_impl(ctx, value, field):
    ctx.resp.form[field] = value

@when(u'I sent the form')
def step_impl(ctx):
    ctx.resp = ctx.resp.form.submit()

@then(u'{text} should be displayed')
def step_impl(ctx, text):
    assert text in ctx.resp