from __future__ import annotations

import os
from typing import BinaryIO, Union

from ..exceptions import SunoAPIError
from ..models import UploadedFile


class UploadResource:
    """Resource manager for the Suno file upload API (separate host, temporary storage)."""

    def __init__(self, client):
        self.client = client

    @staticmethod
    def _validate_upload_response(body: dict, response_text: str) -> dict:
        code = body.get("code")
        if code is not None and int(code) != 200:
            message = body.get("msg") or response_text
            raise SunoAPIError(message, status_code=int(code), response_text=response_text)
        if body.get("success") is False:
            message = body.get("msg") or response_text
            raise SunoAPIError(message, status_code=int(code or 400), response_text=response_text)
        return body

    def _post_json(self, path: str, payload: dict) -> UploadedFile:
        r = self.client.session.post(self.client.upload_base_url + path, json=payload)
        if not r.ok:
            raise SunoAPIError(r.text, status_code=r.status_code, response_text=r.text)
        body = self._validate_upload_response(r.json(), r.text)
        return UploadedFile.from_api_data(body["data"])

    def upload_url(
        self,
        file_url: str,
        upload_path: str,
        file_name: str | None = None,
    ) -> UploadedFile:
        """Upload a remote file by URL."""
        payload: dict = {"fileUrl": file_url, "uploadPath": upload_path}
        if file_name is not None:
            payload["fileName"] = file_name
        return self._post_json("/api/file-url-upload", payload)

    def upload_base64(
        self,
        base64_data: str,
        upload_path: str,
        file_name: str | None = None,
    ) -> UploadedFile:
        """Upload file content as Base64 (best for small files)."""
        payload: dict = {"base64Data": base64_data, "uploadPath": upload_path}
        if file_name is not None:
            payload["fileName"] = file_name
        return self._post_json("/api/file-base64-upload", payload)

    def upload_stream(
        self,
        file: Union[str, BinaryIO, os.PathLike],
        upload_path: str,
        file_name: str | None = None,
    ) -> UploadedFile:
        """Upload a local file via multipart form data."""
        if isinstance(file, (str, os.PathLike)):
            path = os.fspath(file)
            opened_name = file_name or os.path.basename(path)
            with open(path, "rb") as handle:
                return self._upload_stream_handle(handle, opened_name, upload_path)
        opened_name = file_name or getattr(file, "name", "upload.bin")
        if isinstance(opened_name, (str, os.PathLike)):
            opened_name = os.path.basename(os.fspath(opened_name))
        return self._upload_stream_handle(file, opened_name, upload_path)

    def _upload_stream_handle(
        self,
        handle: BinaryIO,
        file_name: str,
        upload_path: str,
    ) -> UploadedFile:
        data = {"uploadPath": upload_path, "fileName": file_name}
        files = {"file": (file_name, handle)}
        headers = {
            key: value
            for key, value in self.client.session.headers.items()
            if key.lower() != "content-type"
        }
        r = self.client.session.post(
            self.client.upload_base_url + "/api/file-stream-upload",
            data=data,
            files=files,
            headers=headers,
        )
        if not r.ok:
            raise SunoAPIError(r.text, status_code=r.status_code, response_text=r.text)
        body = self._validate_upload_response(r.json(), r.text)
        return UploadedFile.from_api_data(body["data"])
