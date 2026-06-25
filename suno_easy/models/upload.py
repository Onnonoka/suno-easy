from dataclasses import dataclass


@dataclass
class UploadedFile:
    """Result of a temporary file upload (auto-deleted after 3 days)."""

    file_name: str
    file_path: str
    download_url: str
    file_size: int
    mime_type: str
    uploaded_at: str

    @classmethod
    def from_api_data(cls, data: dict) -> "UploadedFile":
        return cls(
            file_name=data["fileName"],
            file_path=data["filePath"],
            download_url=data["downloadUrl"],
            file_size=int(data["fileSize"]),
            mime_type=data["mimeType"],
            uploaded_at=data["uploadedAt"],
        )
