from pydantic import BaseModel, Field, field_validator

from src.infrastructure.grpc.generated.order_service_pb2 import OrdersParams



class GetOrdersByUserDto(BaseModel):
    user_id: str = Field(..., description="ID of the user")
    page: int | None = Field(default=None, description="Page number (optional)")
    page_size: int | None = Field(default=None, description="Page size (optional)")
    status: str | None = Field(default=None, description="Filter by order status (optional)")
    sort_order: str | None = Field(default=None, description="Filter by order sort_order (optional)")
    # start_date: datetime | None = Field(default=None, description="Filter orders created after this ISO date (optional)")
    # end_date: datetime | None = Field(default=None, description="Filter orders created before this ISO date (optional)")

    @classmethod
    def from_proto(cls, user_id: str,  proto_obj: OrdersParams):
        # start_date = None
        # end_date = None
        # if getattr(proto_obj, "start_date", None):
        #     start_date = datetime.fromisoformat(proto_obj.start_date)
        # if getattr(proto_obj, "end_date", None):
        #     end_date = datetime.fromisoformat(proto_obj.end_date)
        return cls(
            user_id=user_id,
            page=getattr(proto_obj, "page", None) or None,
            page_size=getattr(proto_obj, "page_size", None) or None,
            status=getattr(proto_obj, "status", None) or None,
            sort_order=getattr(proto_obj, "sort_order", None) or None,
            # start_date=start_date,
            # end_date=end_date
        )

    def to_proto(self) -> OrdersParams:
        proto_obj = OrdersParams()
        if self.sort_order is not None:
            proto_obj.sort_order = self.sort_order
        if self.page is not None:
            proto_obj.page = self.page
        if self.page_size is not None:
            proto_obj.page_size = self.page_size
        if self.status is not None:
            proto_obj.status = self.status
        # if self.start_date is not None:
        #     proto_obj.start_date = self.start_date.isoformat()
        # if self.end_date is not None:
        #     proto_obj.end_date = self.end_date.isoformat()
        return proto_obj

    @field_validator("user_id")
    @classmethod
    def validate_user_id(cls, value):
        if not value or not value.strip():
            raise ValueError("user_id is required and cannot be empty")
        return value

