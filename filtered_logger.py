#!/usr/bin/env python3
"""filtering function"""
import re
from typing import List
import logging
import mysql.connector
from os import getenv


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returnig the log message obfuscated"""
    pattern = fr'(?P<field>{"|".join(fields)})=[^{separator}]*'
    return re.sub(pattern, fr'\g<field>={redaction}', message)


def get_logger() -> logging.Logger:
    """returns a logger object"""
    logger = logging.getLogger('user_data')
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connection object"""
    db_user = getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_host = getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_password = getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_name = getenv('PERSONAL_DATA_DB_NAME', '')

    connection = mysql.connector.connect(user=db_user,
                                         host=db_host,
                                         port=3306,
                                         password=db_password,
                                         database=db_name)

    return connection


def main() -> None:
    """obtain a database connection using get_db and retrieve
    all rows in the users table and display each row under
    a filtered format"""
    fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    columns = fields.split(',')
    query = f"SELECT {fields} FROM users"
    db = get_db()
    logger = get_logger()
    with db.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
        for user in result:
            record = map(lambda x: f'{x[0]}={x[1]}', zip(columns, user))
            message = f'{"; ".join(list(record))};'
            args = ("user_data", logging.INFO, None, None, message, None, None)
            log_record = logging.LogRecord(*args)
            logger.handle(log_record)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """intitializing the class instances"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """a method for overriding the parent class format method"""
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION,
                            message, self.SEPARATOR)


if __name__ == "__main__":
    main()
