# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from pytz import timezone

from odoo import SUPERUSER_ID, _, api, tools

_logger = logging.getLogger(__name__)
tz_montreal = timezone("America/Montreal")


def post_init_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})

        # All demo user is already accepted from list
        adhesion_ids = env["ore.demande.adhesion"].search([])
        for adhesion_id in adhesion_ids:
            adhesion_id.en_attente = False

        # General configuration
        values = {
            "ore_auto_accept_adhesion": True,
            "ore_default_societe": env.ref(
                "demo_ore.societe_sainte_rose_du_nord"
            ).id,
            "ore_default_free_time": 15.0,
        }
        event_config = env["res.config.settings"].sudo().create(values)
        event_config.execute()
