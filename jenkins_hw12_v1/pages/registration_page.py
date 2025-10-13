from datetime import date

from selene import be, have, command, by
from selene import Browser

from jenkins_hw12_v1.models.user import User, Gender, Hobby
from jenkins_hw12_v1.utils import resources


class RegistrationForm:
    def __init__(self, browser: Browser):
        self.browser = browser
        self.first_name = self.browser.element('#firstName')
        self.last_name = self.browser.element('#lastName')
        self.email = self.browser.element('#userEmail')
        self.phone = self.browser.element('#userNumber')
        self.date_input = self.browser.element('#dateOfBirthInput')
        self.subjects_input = self.browser.element('#subjectsInput')
        self.address = self.browser.element('#currentAddress')
        self.state = self.browser.element('#state')
        self.city = self.browser.element('#city')
        self.submit_btn = self.browser.element('#submit')
        self.result_title = self.browser.element('#example-modal-sizes-title-lg')
        self.result_table = self.browser.element('.table')

    # -------- High level --------
    def open(self) -> "RegistrationForm":
        self.browser.open('/automation-practice-form')
        self.first_name.should(be.present)
        return self

    def fill(self, user: User) -> "RegistrationForm":
        self._fill_names(user.first_name, user.last_name)
        self._fill_email(user.email)
        self._select_gender(user.gender)
        self._fill_phone(user.phone)
        self._set_birth_date(user.birth_date)
        self._select_subjects(user.subjects)
        self._select_hobbies(user.hobbies)
        self._upload_picture(user.picture)
        self._fill_address(user.address)
        self._select_state_city(user.state, user.city)
        return self

    def submit(self) -> "RegistrationForm":
        self.submit_btn.perform(command.js.click)
        return self

    def register(self, user: User) -> "RegistrationForm":
        return self.fill(user).submit()

    def should_have_registered(self, user: User) -> "RegistrationForm":
        self.result_title.should(have.exact_text('Thanks for submitting the form'))

        def cell(label: str):
            return self.result_table.element(
                by.xpath(f".//td[normalize-space()='{label}']/following-sibling::td[1]")
            )

        cell('Student Name').should(have.exact_text(user.full_name))
        cell('Student Email').should(have.exact_text(user.email))
        cell('Gender').should(have.exact_text(user.gender.value))
        cell('Mobile').should(have.exact_text(user.phone))
        cell('Date of Birth').should(have.exact_text(user.dob_for_result))
        cell('Subjects').should(have.exact_text(', '.join(user.subjects)))
        cell('Hobbies').should(have.exact_text(', '.join(h.value for h in user.hobbies)))
        cell('Picture').should(have.exact_text(user.picture))
        cell('Address').should(have.exact_text(user.address))
        cell('State and City').should(have.exact_text(f'{user.state} {user.city}'))

        return self

    # -------- Mid level --------
    def _fill_names(self, first: str, last: str) -> None:
        self.first_name.should(be.visible).type(first)
        self.last_name.should(be.visible).type(last)

    def _fill_email(self, value: str) -> None:
        if value:
            self.email.should(be.visible).type(value)

    def _select_gender(self, gender: Gender) -> None:
        mapping = {Gender.male: '1', Gender.female: '2', Gender.other: '3'}
        self.browser.element(f'[for="gender-radio-{mapping[gender]}"]').click()

    def _fill_phone(self, value: str) -> None:
        self.phone.should(be.visible).type(value)

    def _set_birth_date(self, d: date) -> None:
        self.date_input.click()
        self.browser.element('.react-datepicker').should(be.visible)

        # месяц по value
        self.browser.element('.react-datepicker__month-select').click()
        self.browser.element(f'.react-datepicker__month-select option[value="{d.month - 1}"]').click()

        # год по value
        self.browser.element('.react-datepicker__year-select').click()
        self.browser.element(f'.react-datepicker__year-select option[value="{d.year}"]').click()

        # день
        self.browser.element(
            f'.react-datepicker__day--0{d.day:02d}:not(.react-datepicker__day--outside-month)'
        ).click()

    def _select_subjects(self, subjects: list[str]) -> None:
        for s in subjects:
            self.subjects_input.type(s).press_enter()

    def _select_hobbies(self, hobbies: list[Hobby]) -> None:
        mapping = {Hobby.sports: '1', Hobby.reading: '2', Hobby.music: '3'}
        for h in hobbies:
            self.browser.element(f'[for="hobbies-checkbox-{mapping[h]}"]').click()

    def _upload_picture(self, filename: str) -> None:
        if filename:
            self.browser.element('#uploadPicture').set_value(
                resources.resource_path(filename)
            )

    def _fill_address(self, value: str) -> None:
        if value:
            self.address.type(value)

    def _select_state_city(self, state: str, city: str) -> None:
        if state:
            self.state.perform(command.js.scroll_into_view).click()
            self.browser.element('div[class$="-menu"]').should(be.visible)
            self.browser.all('[id^="react-select-3-option-"]').element_by(
                have.exact_text(state)
            ).click()

        if city:
            self.city.click()
            self.browser.element('div[class$="-menu"]').should(be.visible)
            self.browser.all('[id^="react-select-4-option-"]').element_by(
                have.exact_text(city)
            ).click()
