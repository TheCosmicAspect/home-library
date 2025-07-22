from wtforms.fields import SelectField
from wtforms.validators import ValidationError

# Wtforms didn't have a select field that allowed no choices, which is kinda annoying when you have a self-referential model
# Anyway, I present to you, the OptionalSelectField
class OptionalSelectField(SelectField):
    def __init__(self, label=None, validators=None, coerce=str, choices=None, **kwargs):
        super(OptionalSelectField, self).__init__(label, validators, **kwargs)
        self.coerce = coerce
        self.choices = choices or []

    def pre_validate(self, form):
        if not self.validate_choice:
            return

        for _, _, match, *_ in self.iter_choices():
            if match:
                break
        else:
            raise ValidationError(self.gettext("Not a valid choice."))