"""Azure File Storage Manager."""

from azure.storage.fileshare import ShareServiceClient, ShareFileClient
from io import BytesIO
from app.config.afs import AFSENV


class AzureFileStorageManager:
    """Manages file storage operations on Azure, including uploading and downloading files."""

    def __init__(self) -> None:
        """Initialize AzureFileStorageManager with connection settings from AFSENV."""
        self.connection_string = AFSENV.CONNECTION_STRING.value
        self.share_name = AFSENV.SHARE_NAME.value
        self.qr_code_share_name = AFSENV.QR_CODE_SHARE_NAME.value
        self.service_client = ShareServiceClient.from_connection_string(self.connection_string)

    def upload_file(self, file_bytes: bytes, dest_file_path: str) -> None:
        """Upload a file to Azure File Storage.

        Args:
            file_bytes (bytes): The content of the file in bytes.
            dest_file_path (str): The destination path in Azure File Storage.
        """
        file_client = ShareFileClient.from_connection_string(self.connection_string, self.share_name, dest_file_path)
        file_client.upload_file(file_bytes)

    def download_file(self, file_path: str) -> bytes:
        """Download a file from Azure File Storage.

        Args:
            file_path (str): The path of the file in Azure File Storage.

        Returns:
            bytes: The content of the downloaded file.
        """
        file_client = ShareFileClient.from_connection_string(self.connection_string, self.share_name, file_path)

        downloaded_file = file_client.download_file()
        stream = BytesIO()
        downloaded_file.readinto(stream)

        return stream.getvalue()

    def upload_image(self, local_image_path: str, dest_file_path: str, file_share: str) -> None:
        """Upload a QR code image to Azure file Storage.

        Args:
            local_image_path (bytes): The QR code image path.
            dest_file_path (str): The destination path in Azure file Storage.
            file_share: azure file share name.

        """
        file_client = ShareFileClient.from_connection_string(self.connection_string, file_share, dest_file_path)
        source_file = open(local_image_path, "rb")
        data = source_file.read()
        file_client.upload_file(data)
