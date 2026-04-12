"""E-Mail versenden."""
from email.mime.text import MIMEText
from email.utils import make_msgid
from smtplib import SMTP, SMTPServerDisconnected
from socket import gaierror
from typing import Final
from uuid import uuid4

from loguru import logger

from krankenhaus.config import mail_enabled, mail_host, mail_port, mail_timeout
from krankenhaus.service import KrankenhausDTO

__all__ = ["send_mail"]

MAILSERVER: Final = mail_host
PORT: Final = mail_port
SENDER: Final = "Python Server <python.server@acme.com>"
RECEIVER: Final = ["Krankenhaus Verwaltung <verwaltung@acme.com>"]
TIMEOUT: Final = mail_timeout


def send_mail(krankenhaus_dto: KrankenhausDTO) -> None:
    """Versenden einer E-Mail.

    :param krankenhaus_dto: Krankenhaus-Informationen
    """
    logger.debug("{}", krankenhaus_dto)
    if not mail_enabled:
        logger.warning("send_mail: Der Mailserver ist nicht aktiviert")
        return

    msg: Final = MIMEText(f"Neues Krankenhaus: <b>{krankenhaus_dto}</b>")
    msg["Subject"] = f"Neues Krankenhaus: ID={krankenhaus_dto.id}"
    msg["Message-ID"] = make_msgid(idstring=str(uuid4()))

    try:
        logger.debug("Verbinde mit Mailserver {}:{}", MAILSERVER, PORT)
        with SMTP(host=MAILSERVER, port=PORT, timeout=TIMEOUT) as smtp:
            smtp.sendmail(from_addr=SENDER, to_addrs=RECEIVER, msg=msg.as_string())
            logger.debug("msg={}", msg)
    except ConnectionRefusedError:
        logger.warning("send_mail: ConnectionRefusedError")
    except SMTPServerDisconnected:
        logger.warning("send_mail: SMTPServerDisconnected")
    except gaierror:
        logger.warning("send_mail: gaierror")
