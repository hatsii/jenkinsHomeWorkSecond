import allure
from jenkinshomeworksecond.pages.registration_page import RegistrationForm
from jenkinshomeworksecond.data import users

def test_registration_with_preset_user(setup_browser):
    form = RegistrationForm(setup_browser)

    with allure.step("Open registration page"):
        form.open()

    with allure.step("Fill and submit registration form"):
        form.register(users.student)

    with allure.step("Verify registration results"):
        form.should_have_registered(users.student)
