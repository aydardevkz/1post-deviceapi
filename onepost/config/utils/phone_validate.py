import re

country_phone = [
    {
        "code": "7",
        "length": 10,
        "pattern": r'^7([057][0125678]\d{7})$',
    }
]


class PhoneValidate:
    @staticmethod
    def validate_country_code(country_code):
        for country in country_phone:
            if country['code'] == country_code:
                return True
        return False

    @staticmethod
    def validate_phone(phone, country_code):
        for country in country_phone:
            if country['code'] == country_code:
                if re.match(country['pattern'], phone):
                    return True
                else:
                    return False
        return False
