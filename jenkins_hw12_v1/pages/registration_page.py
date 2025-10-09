from selene.support.shared import browser
from selene import be, have, command, query,by
from datetime import date

from jenkins_hw12_v1.models.user import User, Gender, Hobby
from jenkins_hw12_v1.utils import resources


class RegistrationForm:
    def __init__(self):
        self.first_name = browser.element('#firstName')
        self.last_name = browser.element('#lastName')
        self.email = browser.element('#userEmail')
        self.phone = browser.element('#userNumber')
        self.date_input = browser.element('#dateOfBirthInput')
        self.subjects_input = browser.element('#subjectsInput')
        self.address = browser.element('#currentAddress')
        self.state = browser.element('#state')
        self.city = browser.element('#city')
        self.submit_btn = browser.element('#submit')
        self.result_title = browser.element('#example-modal-sizes-title-lg')
        self.result_table = browser.element('.table')

    # Высокий уровень
    def open(self):
        browser.open('/automation-practice-form')
        browser.element('#firstName').should(be.present)
        return self

    def fill(self, user: User):
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

    def submit(self):
        self.submit_btn.perform(command.js.click)
        return self

    def register(self, user: User):
        return self.fill(user).submit()

    def should_have_registered(self, user: User):
        self.result_title.should(have.exact_text('Thanks for submitting the form'))
        def cell(label: str):
            return self.result_table.element(
                by.xpath(f".//td[normalize-space()='{label}']/following-sibling::td[1]")
            )

        cell('Student Name').should(have.exact_text(user.full_name))
        cell('Student Email').should(have.exact_text(user.email))
        cell('Gender').should(have.exact_text(user.gender.value))
        cell('Mobile').should(have.exact_text(user.phone))
        cell('Date of Birth').should(have.exact_text(user.dob_for_result))  # '15 March,2000'
        cell('Subjects').should(have.exact_text(', '.join(user.subjects)))
        cell('Hobbies').should(have.exact_text(', '.join(h.value for h in user.hobbies)))
        cell('Picture').should(have.exact_text(user.picture))
        cell('Address').should(have.exact_text(user.address))
        cell('State and City').should(have.exact_text(f'{user.state} {user.city}'))

        return self

    # Средний уровень
    def _fill_names(self, first: str, last: str):
        self.first_name.should(be.visible).type(first)
        self.last_name.should(be.visible).type(last)

    def _fill_email(self, value: str):
        if value:
            self.email.should(be.visible).type(value)

    def _select_gender(self, gender: Gender):
        mapping = {Gender.male: '1', Gender.female: '2', Gender.other: '3'}
        browser.element(f'[for="gender-radio-{mapping[gender]}"]').click()

    def _fill_phone(self, value: str):
        self.phone.should(be.visible).type(value)

    def _set_birth_date(self, d:date):
        self.date_input.click()
        browser.element('.react-datepicker').should(be.visible)
        # месяц
        browser.element('.react-datepicker__month-select').click()
        browser.all('.react-datepicker__month-select option') \
            .element_by(have.exact_text(d.strftime('%B'))).click()
        # год
        browser.element('.react-datepicker__year-select').click()
        browser.all('.react-datepicker__year-select option') \
            .element_by(have.exact_text(str(d.year))).click()
        # день
        day_str = f'{d.day:02d}'
        browser.element(
            f'.react-datepicker__day--0{day_str}:not(.react-datepicker__day--outside-month)'
        ).click()


    def _select_subjects(self, subjects: list[str]):
        for s in subjects:
            self.subjects_input.type(s).press_enter()

    def _select_hobbies(self, hobbies: list[Hobby]):
        mapping = {Hobby.sports: '1', Hobby.reading: '2', Hobby.music: '3'}
        for h in hobbies:
            browser.element(f'[for="hobbies-checkbox-{mapping[h]}"]').click()

    def _upload_picture(self, filename: str):
        if filename:
            browser.element('#uploadPicture').set_value(resources.resource_path(filename))

    def _fill_address(self, value: str):
        if value:
            self.address.type(value)

    def _select_state_city(self, state: str, city: str):
        if state:
            self.state.perform(command.js.scroll_into_view).click()
            browser.element('div[class$="-menu"]').should(be.visible)
            browser.all('[id^="react-select-3-option-"]').element_by(have.exact_text(state)).click()

        if city:
            self.city.click()
            browser.element('div[class$="-menu"]').should(be.visible)
            browser.all('[id^="react-select-4-option-"]').element_by(have.exact_text(city)).click()
