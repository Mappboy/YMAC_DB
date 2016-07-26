from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import re
import os


def valid_surveyid(value):
    valid_survey = re.compile(r'[A-Z&]{3}\d{3}-\d{1,5}')
    match = valid_survey.match(value)
    if not match or not match.group(0) == value:
        raise ValidationError(
            _('%(value)s does not match CLM000-1'),
            params={'value': value},
        )

def valid_directory(value):
    if not os.path.isdir(value):
        raise ValidationError(
            _('%(value)s is not a valid directory'),
            params={'value': value},
        )
