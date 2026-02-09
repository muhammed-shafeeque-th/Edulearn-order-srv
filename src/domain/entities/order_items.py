from dataclasses import dataclass
from typing import Any



@dataclass
class OrderItem:
    id: str
    course_id: str
    price: float

    @classmethod
    def create(
        cls, id: str, course_id: str, price: float
    ) -> "OrderItem":
        return cls(
            id=id,
            course_id=course_id,
            price=price,
        )

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "course_id": self.course_id, "price": self.price}
