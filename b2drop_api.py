from pathlib import Path
import hashlib
import tempfile
import os

from webdav3.client import Client
from webdav3.exceptions import RemoteResourceNotFound

from typing import Union, Optional


class B2dropClient:
    def __init__(self, url: str, username: str, password: str):
        if url.endswith("/"):
            url = url[:-1]
        self.base_url = f"{url}/remote.php/dav/files/{username}/"
        self.temp_dir = tempfile.TemporaryDirectory()
        self.dummy_file = "dummy.txt"
        options = {
            'webdav_hostname': self.base_url,
            'webdav_login': username,
            'webdav_password': password,
            # 'webdav_override_methods': {
            #    'check': 'GET'
            # }
        }
        self.client = Client(options)

        self.client.verify = True  # To not check SSL certificates (Default = True)
        # self.client.session.proxies(...)  # To set proxy directly into the session (Optional)
        # self.client.session.auth(...)  # To set proxy auth directly into the session (Optional)
        if not self.logged_in():
            message = f"Username or password wrong, please go to {url}/settings/user/security and create an app token and \
                update your config.json OR username/password parameters"
            logger.error(message)
            print ("CRITICAL: Username or password wrong, please go to {url}/settings/user/security and create an app token and \
                update your config.json OR username/password parameters")
            sys.exit(2)
            
        else:
            logger.info("API Client ready to use")


    def cleanup(self):
        self.delete(self.dummy_file)
        self.temp_dir.cleanup()

    def __del__(self):
        self.temp_dir.cleanup()

    def create_dummy_file(self) -> Path:
        """
        creates a local dummy file named dummy.txt
        :return: temp path of the dummy file
        """
        file_path = os.path.join(self.temp_dir.name, self.dummy_file)
        content = "dummy content"
        with open(file_path, 'w') as temp_file:
            temp_file.write(content)
        return Path(file_path)

    def upload(self, filename: Union[str, Path], remote_directory: Optional[str] = None) -> Path:
        """
        upload a local path to a remote directory
        :param remote_directory: b2drop directory where to put the file to
        :param filename: filename and path of a local path
        :return: remote Path (unchecked)
        """
        filename = Path(filename)
        if remote_directory:
            self.client.upload_sync(remote_path=remote_directory, local_path=str(filename))
            remote_path = os.path.join(remote_directory, filename.name)
        else:
            self.client.upload_sync(
                remote_path=filename.name,
                local_path=str(filename))
            remote_path = Path(filename.name)
        return Path(remote_path)

    def download(self, filename: Union[str, Path]) -> Path:
        """
        downloads a file from b2drop to a temp-directory
        :param filename: path and filename of a file
        :return: local Path of the downloaded file
        """
        filename = Path(filename)
        local_path = os.path.join(self.temp_dir.name, filename.name)
        self.client.download_sync(remote_path=str(filename), local_path=local_path)
        return Path(local_path)

    @staticmethod
    def get_checksum(filename: Union[str, Path]) -> str:
        """
        Returns the md5 checksum of a local file
        :param filename: path and filename of a file
        :return: md5 checksum as hex string
        """
        file = Path(filename)
        assert file.exists()
        # Open,close, read file and calculate MD5 on its contents
        with open(str(file), 'rb') as file_to_check:
            # read contents of the file
            data = file_to_check.read()
            # pipe contents of the file through
            md5_returned = hashlib.md5(data).hexdigest()
        return md5_returned

    def delete(self, filename: Union[str, Path]) -> bool:
        """
        Delete a file from b2drop
        :param filename: path and filename of a file
        :return: true if file doesn't exist
        """
        if self.file_exists(str(filename)):
            self.client.clean(str(filename))
        return not self.file_exists(filename)

    def file_exists(self, filename: Union[str, Path]) -> bool:
        """
        Checks if a file exists on b2drop
        :param filename: path and filename of a file
        :return: bool
        """
        try:
            ret = self.client.check(str(filename))
            return ret
        except RemoteResourceNotFound as e:
            raise ValueError("Remote url unreachable") from e
