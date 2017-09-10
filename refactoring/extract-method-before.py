class RegistrationFormTests(unittest.TestCase):
    def test_successful_submission(self):
        form = self.app.get('/register').form

        # fill in the form
        form['personal'] = 'John'
        form['family'] = 'Smith'
        form['email'] = 'john@smith.com'
        form['location'] = 'Cracow'
        form['country'] = 'PL'
        form['agreed_to_code_of_conduct'] = True
        form['recaptcha_response_field'] = 'PASSED'

        response = form.submit()

        self.assertEqual(response.status_code, 200)
