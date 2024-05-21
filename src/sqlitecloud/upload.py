from io import BufferedReader
import os
from typing import Optional
from sqlitecloud.driver import Driver
from sqlitecloud.types import SQCloudConnect
import logging

def xCallback(fd: BufferedReader, blen: int, ntot: int, nprogress: int) -> bytes:
    """
    Callback function used for uploading data.

    Args:
        fd (BufferedReader): The file descriptor to read data from.
        blen (int): The length of the buffer to read.
        ntot (int): The total number of bytes to be uploaded.
        nprogress (int): The number of bytes already uploaded.

    Returns:
        bytes: The buffer containing the read data.
    """
    buffer = fd.read(blen)
    nread = len(buffer)

    if nread == 0:
        logging.log(logging.DEBUG, "UPLOAD COMPLETE\n\n")
    else:
        logging.log(logging.DEBUG, f"{(nprogress + nread) / ntot * 100:.2f}%")

    return buffer


def upload_db(
    connection: SQCloudConnect, dbname: str, key: Optional[str], filename: str
) -> None:
    """
    Uploads a SQLite database to the SQLite Cloud node using the provided connection.

    Args:
        connection (SQCloudConnect): The connection object used to connect to the node.
        dbname (str): The name of the database in SQLite Cloud.
        key (Optional[str]): The encryption key for the database. If None, no encryption is used.
        filename (str): The path to the SQLite database file to be uploaded.

    Raises:
        SQCloudException: If an error occurs while uploading the database.

    """
    
    # Create a driver object
    driver = Driver()

    with open(filename, 'rb') as fd:
        dbsize = os.path.getsize(filename)

        driver.upload_database(
            connection,
            dbname,
            key,
            False,
            0,
            False,
            fd,
            dbsize,
            xCallback,
        )
