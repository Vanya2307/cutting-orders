import re
from django.core.exceptions import ValidationError



def normalize_phone(value):
        
    phone = re.sub(r'[\s()-]', '', value or '')

    if phone.startswith('+359'):
        phone = phone[4:]

    if phone.startswith('0'):
        phone = phone[1:]

    if not re.fullmatch(r'[89][0-9]{8}', phone):
        raise ValidationError(
            'Моля, въведете валиден български мобилен номер.'
        )

    return f'+359{phone}'