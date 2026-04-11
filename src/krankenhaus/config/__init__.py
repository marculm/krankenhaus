"""Modul zur Konfiguration."""

from krankenhaus.config.db import (
    db_connect_args,
    db_dialect,
    db_log_statements,
    db_url,
    db_url_admin,
)
from krankenhaus.config.dev_modus import dev_db_populate, dev_keycloak_populate
from krankenhaus.config.excel import excel_enabled
from krankenhaus.config.graphql import graphql_ide
from krankenhaus.config.keycloak import (
    csv_config,
    keycloak_admin_config,
    keycloak_config,
)
from krankenhaus.config.logger import config_logger
from krankenhaus.config.mail import (
    mail_enabled,
    mail_host,
    mail_port,
    mail_timeout,
)
from krankenhaus.config.server import host_binding, port
from krankenhaus.config.tls import tls_certfile, tls_keyfile

__all__ = [
    "config_logger",
    "csv_config",
    "db_connect_args",
    "db_dialect",
    "db_log_statements",
    "db_url",
    "db_url_admin",
    "dev_db_populate",
    "dev_keycloak_populate",
    "excel_enabled",
    "graphql_ide",
    "host_binding",
    "keycloak_admin_config",
    "keycloak_config",
    "mail_enabled",
    "mail_host",
    "mail_port",
    "mail_timeout",
    "port",
    "tls_certfile",
    "tls_keyfile",
]
