from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class OrderCreateDto(BaseModel):
    user_id: str = Field(..., description="ID of the user placing the order")
    course_ids: list[str] = Field(..., description="List of course IDs to order")
    coupon_code: str | None = Field(
        default=None, description="ID of coupon if Present"
    )

    @field_validator("course_ids")
    def validate_course_ids(cls, value):
        if not all(
            isinstance(course_id, str) and course_id.strip() for course_id in value
        ):
            raise ValueError("All course IDs must be non-empty strings")
        return value
