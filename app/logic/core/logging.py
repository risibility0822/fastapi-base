from app import log
import time
from starlette.requests import Request
from starlette.responses import Response
from typing import Callable
import os
import logging
from colorlog import ColoredFormatter


class APILog:
    """
    專門處理API Log 的 class (Middleware).

    Attributes:
        LOG_MAX_BODY_SIZE: log body 的最大長度
    """

    LOG_MAX_BODY_SIZE = 1000

    def __init__(self) -> None:
        """Init."""
        pass

    async def __call__(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        """
        提供給 middleware 的 callback 函式.

        Args:
            request: Starlette 框架的請求對象，包含請求的詳細信息
            call_next: 下一個中間件或請求處理器的函數，用於獲取當前請求的響應

        Returns:""
        """
        start_time = time.time()
        request_info = {}
        response_info = {}

        try:
            # 蒐集 request 資訊
            request_body = await request.body()
            request_info = {
                "url": str(request.url),
                "method": request.method,
                "headers": dict(request.headers),
                "body": request_body[: self.LOG_MAX_BODY_SIZE].decode("utf-8", errors="ignore"),
            }
            if len(request_body) > self.LOG_MAX_BODY_SIZE:
                request_info["body"] += " (truncated)"

            # 執行 request 然後取得 response
            response = await call_next(request)

            # 蒐集 response 資訊
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk

            duration = time.time() - start_time
            response_info = {
                "status_code": response.status_code,
                "duration": f"{duration:.2f} seconds",
                "body": response_body[: self.LOG_MAX_BODY_SIZE].decode("utf-8", errors="ignore"),
            }
            if len(response_body) > self.LOG_MAX_BODY_SIZE:
                response_info["body"] += " (truncated)"

        except Exception as ex:
            response_info = {
                "status_code": "500",
                "duration": f"{time.time() - start_time:.2f} seconds",
                "body": "Internal Server Error",
            }
            log.critical(ex, exc_info=True)

        finally:
            log_message = (
                f"{request_info.get('method', 'UNKNOWN')} {request_info.get('url', 'UNKNOWN')}"
                f" - {response_info.get('status_code', 'UNKNOWN')}\n"
                f"<<< Request >>>\n"
                f"URL: {request_info.get('url', 'UNKNOWN')}\n"
                f"Method: {request_info.get('method', 'UNKNOWN')}\n"
                f"Headers: {request_info.get('headers', 'UNKNOWN')}\n"
                f"Body: {request_info.get('body', 'UNKNOWN')}\n"
                f"<<< Response >>>\n"
                f"Status Code: {response_info.get('status_code', 'UNKNOWN')}\n"
                f"Duration: {response_info.get('duration', 'UNKNOWN')}\n"
                f"Body: {response_info.get('body', 'UNKNOWN')}"
            )
            log.debug(log_message)

        return Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )


class CustomColoredFormatter(ColoredFormatter):
    """Customized ColoredFormatter

    Args:
        ColoredFormatter (_type_): ColoredFormatter
    """

    def format(self, record: logging.LogRecord) -> str:
        """Format log record

        Args:
            record (logging.LogRecord): LogRecord

        Returns:
            str: Formatted log record
        """
        record.black = "\033[30m"
        record.red = "\033[31m"
        record.green = "\033[32m"
        record.yellow = "\033[33m"
        record.blue = "\033[34m"
        record.magenta = "\033[35m"
        record.cyan = "\033[36m"
        record.white = "\033[37m"
        record.reset = "\033[0m"

        parent_dir = os.path.basename(os.path.dirname(record.pathname))
        record.parent_filename = parent_dir

        return super().format(record)


class CustomFormatter(logging.Formatter):
    """Customized Formatter

    Args:
        logging (_type_): Formatter
    """

    def format(self, record: logging.LogRecord) -> str:
        """Format log record

        Args:
            record (logging.LogRecord): LogRecord

        Returns:
            str: Formatted log record
        """
        parent_dir = os.path.basename(os.path.dirname(record.pathname))
        record.parent_filename = parent_dir
        return super().format(record)


class InfoOnlyFilter(logging.Filter):
    """Filter out log records with levelno other than INFO

    Args:
        logging (_type_): Filter
    """

    def filter(self, record: logging.LogRecord) -> bool:
        """Filter out log records with levelno other than INFO

        Args:
            record (logging.LogRecord): LogRecord

        Returns:
            bool: True if levelno is INFO, False otherwise
        """
        return record.levelno == logging.INFO
