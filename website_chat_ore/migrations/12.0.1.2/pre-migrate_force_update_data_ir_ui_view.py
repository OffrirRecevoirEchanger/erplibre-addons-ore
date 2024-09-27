import logging

import odoo
from odoo import SUPERUSER_ID, api
from odoo.tools import parse_version

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    if parse_version(version) == parse_version("12.0.1.0"):
        registry = odoo.registry(cr.dbname)
        env = api.Environment(cr, SUPERUSER_ID, {})
        # Delete this view will force to update it
        view_id = env["ir.ui.view"].search(
            [
                (
                    "key",
                    "=",
                    "website_chat_ore.ir_ui_view_messages_et_notifications_inherit",
                )
            ]
        )
        view_id.unlink()
        _logger.info("End of pre migrate_force_update_data_ir_ui_view")
