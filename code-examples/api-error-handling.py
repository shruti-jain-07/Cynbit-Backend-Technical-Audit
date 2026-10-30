from dataclasses import dataclass
from uuid import uuid4


@dataclass
class ApiError:
    code: str
    message: str
    request_id: str
    fields: dict[str, str] | None = None

    def to_dict(self) -> dict:
        error = {
            "code": self.code,
            "message": self.message,
            "requestId": self.request_id,
        }
        if self.fields:
            error["fields"] = self.fields
        return {"success": False, "error": error}


def validation_error_response(fields: dict[str, str]) -> tuple[int, dict]:
    request_id = str(uuid4())
    body = ApiError(
        code="VALIDATION_ERROR",
        message="Please check the submitted fields.",
        request_id=request_id,
        fields=fields,
    )
    return 400, body.to_dict()


def internal_error_response() -> tuple[int, dict]:
    # Do not expose exception text, stack traces, SQL, or filesystem paths.
    request_id = str(uuid4())
    body = ApiError(
        code="INTERNAL_ERROR",
        message="Something went wrong. Please try again later.",
        request_id=request_id,
    )
    # A real service should log diagnostic details securely with request_id.
    return 500, body.to_dict()


if __name__ == "__main__":
    print(validation_error_response({"email": "Enter a valid email address."}))
    print(internal_error_response())
