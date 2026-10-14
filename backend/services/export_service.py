"""Google Drive document export helpers."""

import io
from googleapiclient.http import MediaIoBaseDownload

EXPORT_MIME_TYPES = {
    "pdf": "application/pdf",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


def export_google_doc(file_id: str, drive_service, output_format: str = "pdf") -> bytes:
    """Export a Google Doc from Drive as PDF or DOCX and return its bytes."""
    mime_type = EXPORT_MIME_TYPES.get(output_format.lower())
    if not mime_type:
        raise ValueError("output_format must be 'pdf' or 'docx'")

    request = drive_service.files().export_media(fileId=file_id, mimeType=mime_type)
    buffer = io.BytesIO()
    downloader = MediaIoBaseDownload(buffer, request)

    done = False
    while not done:
        _, done = downloader.next_chunk()

    buffer.seek(0)
    return buffer.read()
