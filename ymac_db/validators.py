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

def valid_extension(value):
    if not os.path.splitext(value)[1]:
        raise ValidationError(
            _('%(value)s has no extension. Bad File.'),
            params={'value': value},
        )

def valid_job_number(value):
    if value and not 2000 <= int(value[1:5]) <= 3000:
        raise ValidationError(
            _('%(value)s has no extension. Bad File.'),
            params={'value': value},
        )