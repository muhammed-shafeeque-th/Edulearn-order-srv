from src.application.interfaces.logging_interface import ILoggingService
from src.application.interfaces.auth_guard_interface import IAuthGuard
from src.application.interfaces.grpc_client_interface import IUserServiceClient
from jose import jwt
from jose.exceptions import JWTError
from src.infrastructure.config.settings import settings
import logging


class AuthGuard(IAuthGuard):
    def __init__(self, user_service_client: IUserServiceClient, logging_service: ILoggingService):
        self.user_service_client = user_service_client
        self.logger = logging_service.get_logger("AuthGuard")
        self.secret_key = settings.JWT_SECRET

    async def validate_token(self, token: str | bytes) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            user_id = payload.get("sub")
            if not user_id:
                self.logger.error("Invalid JWT token: missing 'sub' claim")
                raise ValueError("Invalid JWT token")

            return {
                "user_id": user_id,
                "role": payload.get("role"),

            }

            # user_info = await self.user_service_client.get_user(user_id)
            # if user_info["user_id"] != user_id:
            #     self.logger.error("User verification failed")
            #     raise ValueError("User verification failed")
            # return user_info
        except JWTError as e:
            self.logger.error(f"JWT decoding failed: {str(e)}")
            raise ValueError("Invalid JWT token")
        except Exception as e:
            self.logger.error(f"Authentication failed: {str(e)}")
            raise

    async def authorize(self, user_info: dict, required_role: str = "STUDENT") -> None:
        role = user_info.get("role")
        if role != required_role:
            self.logger.error(
                f"Authorization failed: user role {role} does not match required role {required_role}")
            raise ValueError(
                f"User role {role} not authorized for this action")
