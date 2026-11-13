"""Format error API yang konsisten: {message, errors:{field: pesan}}."""

from typing import NoReturn

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

FIELD_LABELS = {
    "entityId": "entityId",
    "entity_id": "entityId",
    "visitDate": "visitDate",
    "visit_date": "visitDate",
    "segment": "segment",
    "status": "status",
    "username": "username",
    "password": "password",
    "from": "from",
    "to": "to",
    "search": "search",
}


def api_error(
    status_code: int,
    message: str,
    errors: dict[str, str] | None = None,
    headers: dict[str, str] | None = None,
) -> NoReturn:
    raise HTTPException(
        status_code=status_code,
        detail={"message": message, "errors": errors or {}},
        headers=headers,
    )


def _indonesian_message(error: dict) -> str:
    error_type = error.get("type", "")
    loc = error.get("loc", ())
    field = str(loc[-1]) if loc else ""

    if error_type in {"missing", "string_too_short"}:
        return "Wajib diisi."
    if error_type == "literal_error":
        if field == "status":
            return "Status harus VISITED atau NOT_VISITED."
        if field == "segment":
            return "Segmen harus B2G atau B2B."
    if error_type in {"date_from_datetime_parsing", "date_parsing", "date_type"}:
        return "Tanggal harus format YYYY-MM-DD."
    if error_type == "string_type":
        return "Harus berupa teks."
    if error_type in {"int_parsing", "int_type"}:
        return "Harus berupa angka."
    return "Nilai tidak valid."


async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    detail = exc.detail
    if isinstance(detail, dict) and "message" in detail:
        content = {
            "message": detail["message"],
            "errors": detail.get("errors", {}),
        }
    else:
        content = {"message": str(detail), "errors": {}}
    return JSONResponse(
        status_code=exc.status_code, content=content, headers=exc.headers
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    errors: dict[str, str] = {}
    for error in exc.errors():
        loc = error.get("loc", ())
        key = str(loc[-1]) if loc else "body"
        key = FIELD_LABELS.get(key, key)
        errors.setdefault(key, _indonesian_message(error))

    return JSONResponse(
        status_code=422,
        content={
            "message": "Data yang dikirim tidak valid.",
            "errors": errors,
        },
    )
