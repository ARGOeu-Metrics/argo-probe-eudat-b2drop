from b2drop_api import B2dropClient

import os
import logging

logger = logging.getLogger(__name__)


def probe_upload(client: B2dropClient):
    dummy_path = client.create_dummy_file()

    logger.info("Uploading dummy file")
    dummy_path_remote = client.upload(dummy_path)
    ret = client.file_exists(dummy_path_remote)

    logger.info(f"Upload {'successful' if ret else 'unsuccessful'}")
    return ret


def probe_up_and_download(client: B2dropClient):
    dummy_path = client.create_dummy_file()

    logger.info("Uploading dummy file")
    dummy_path_remote = client.upload(dummy_path)

    if not client.file_exists(dummy_path_remote):
        logger.warning("Upload unsuccessful")
        return False
    logging.info("Upload successful")

    os.rename(str(dummy_path), os.path.join(client.temp_dir.name, "dummy2.txt"))

    logger.info("Downloading dummy file")
    new_path = client.download(dummy_path_remote)

    ret = new_path.exists()
    logger.info(f"Download {'successful' if ret else 'unsuccessful'}")
    return ret


def probe_checksum(client: B2dropClient):
    dummy_path = client.create_dummy_file()
    md5_checksum_old = client.get_checksum(dummy_path)

    logger.info("Uploading dummy file")
    dummy_path_remote = client.upload(dummy_path)
    if not client.file_exists(dummy_path_remote):
        logger.warning("Upload unsuccessful")
        return False

    os.rename(str(dummy_path), os.path.join(client.temp_dir.name, "dummy2.txt"))

    logger.info("Downloading dummy file")
    new_path = client.download(dummy_path_remote)
    if not new_path.exists():
        logger.warning("Download unsuccessful")
        return False

    logger.info("Download successful")
    md5_checksum_new = client.get_checksum(new_path)
    md5_comp = md5_checksum_new == md5_checksum_old
    logger.info(f"MD5 match: {md5_comp}")
    return md5_comp

def probe_all_actions(client: B2dropClient):
    dummy_path = client.create_dummy_file()
    md5_checksum_old = client.get_checksum(dummy_path)

    logger.info("Uploading dummy file")
    dummy_path_remote = client.upload(dummy_path)

    if not client.file_exists(dummy_path_remote):
        logger.warning("Upload unsuccessful")
        return False
    logging.info("Upload successful")

    os.rename(str(dummy_path), os.path.join(client.temp_dir.name, "dummy2.txt"))

    logger.info("Downloading dummy file")
    new_path = client.download(dummy_path_remote)
    if not new_path.exists():
        logger.warning("Download unsuccessful")
        return False
    logging.info("Download successful")

    logger.info("Deleting dummy file")
    client.delete(dummy_path_remote)
    exists = client.file_exists(dummy_path_remote)
    if not client.file_exists(dummy_path_remote):
        logger.warning("Deletion unsuccessful")
        return False
    logging.info("Deletion successful")
    
    logger.info("Check checksum")
    md5_checksum_new = client.get_checksum(new_path)
    md5_comp = md5_checksum_new == md5_checksum_old
    logger.info(f"MD5 match: {md5_comp}")
    return md5_comp

def probe_delete(client: B2dropClient):
    dummy_path = client.create_dummy_file()

    logger.info("Uploading dummy file")
    dummy_path_remote = client.upload(dummy_path)
    
    if not client.file_exists(dummy_path_remote):
        logger.warning("Upload unsuccessful")
        return False
    logging.info("Upload successful")

    logger.info("Deleting dummy file")
    client.delete(dummy_path_remote)
    exists = client.file_exists(dummy_path_remote)
    logger.info(f"Deletion {'successful' if not exists else 'unsuccessful'}")
    return not exists
