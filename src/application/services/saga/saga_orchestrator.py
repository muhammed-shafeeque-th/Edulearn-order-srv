import logging
from typing import Any
from src.application.interfaces.logging_interface import ILoggingService
from src.application.interfaces.metrics_interface import IMetricsService
from src.application.services.interfaces.saga_step import SagaStep
from tenacity import retry, stop_after_attempt, wait_exponential


class SagaOrchestrator:
    def __init__(self, steps: list[SagaStep],  logging_service: ILoggingService, metrics: IMetricsService) -> None:
        self.steps = steps
        self.metrics = metrics
        self.logger = logging_service.get_logger("SagaOrchestrator")
        self.context: dict[str, Any] = {}

    async def execute(self):
        for step in self.steps:
            try:
                self.logger.info(
                    f"Executing SAGA step: {step.__class__.__name__}")
                await self._execute_with_retry(step)

            except Exception as e:
                self.logger.error(
                    f"SAGA step {step.__class__.__name__} failed: {str(e)}")
                self.metrics.saga_failures(step=step.__class__.__name__)
                await self.compensate()
                raise
            self.logger.info("SAGA completed successfully")

    async def compensate(self):
        for step in reversed(self.steps):
            try:
                self.logger.info(
                    f"Compensating SAGA step: {step.__class__.__name__}")
                await step.compensate(self.context)
            except Exception as e:
                self.logger.error(
                    f"Compensation failed for step {step.__class__.__name__}: {str(e)}")

    async def _execute_with_retry(self, step: SagaStep):
        @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
        async def execute_step():
            await step.execute(self.context)
        await execute_step()
