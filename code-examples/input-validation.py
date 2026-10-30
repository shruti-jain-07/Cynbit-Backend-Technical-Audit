from dataclasses import dataclass
import re


@dataclass
class ContactInput:
    full_name: str
    email: str
    company: str = ""
    industry: str = ""
    message: str = ""


class ValidationError(ValueError):
    def __init__(self, fields: dict[str, str]):
        super().__init__("Input validation failed")
        self.fields = fields


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")



def validate_contact_payload(payload: dict) -> ContactInput:
    # Illustrative server-side validation. Adapt limits to product requirements.
    allowed = {"fullName", "email", "company", "industry", "message"}
    unexpected = set(payload) - allowed
    if unexpected:
        raise ValidationError({"request": "Unexpected fields were supplied."})

    errors = {}

    def read_string(key: str, required: bool, max_length: int) -> str:
        value = payload.get(key, "")
        if not isinstance(value, str):
            errors[key] = "Must be a string."
            return ""
        value = value.strip()
        if required and not value:
            errors[key] = "This field is required."
        if len(value) > max_length:
            errors[key] = f"Must be at most {max_length} characters."
        return value

    full_name = read_string("fullName", True, 100)
    email = read_string("email", True, 254)
    company = read_string("company", False, 120)
    industry = read_string("industry", False, 80)
    message = read_string("message", True, 5000)

    if full_name and len(full_name) < 2:
        errors["fullName"] = "Must contain at least 2 characters."
    if email and not EMAIL_PATTERN.fullmatch(email):
        errors["email"] = "Enter a valid email address."
    if message and len(message) < 10:
        errors["message"] = "Must contain at least 10 characters."

    if errors:
        raise ValidationError(errors)

    return ContactInput(full_name, email, company, industry, message)




if __name__ == "__main__":
    sample = {
        "fullName": "Alex Rivera",
        "email": "alex@example.com",
        "company": "Example Ltd",
        "industry": "Fintech",
        "message": "We would like to discuss a software project.",
    }

    try:
        result = validate_contact_payload(sample)
        print(result)
    except ValidationError as error:
        print("Validation failed:", error.fields)
