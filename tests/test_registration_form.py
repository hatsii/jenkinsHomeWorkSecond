import allure
from jenkins_hw12_v1.pages.registration_page import RegistrationForm
from jenkins_hw12_v1.data import users

def test_registration_with_preset_user(app):
    form = RegistrationForm(app)

    with allure.step("Open registration page"):
        form.open()

    with allure.step("Fill and submit registration form"):
        form.register(users.student)

    with allure.step("Verify registration results"):
        form.should_have_registered(users.student)
