# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
import logging

from odoo import SUPERUSER_ID, _, api, tools

_logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})

        company_id = env["res.partner"].browse(env.ref("base.main_company").id)
        company_id.website = "https://ore.quebec"
        company_id.name = "ORE"
        company_id.email = "info@ore.quebec"
        company_id.city = "Québec"
        company_id.country_id = env.ref("base.ca")
        company_id.state_id = env["res.country.state"].search(
            [("code", "ilike", "QC")], limit=1
        )

        company_id = env["res.company"].browse(1)
        # Force sequence 1, the warehouse will be first will multi-company
        company_id.sequence = 1

        user_admin_id = env["res.partner"].browse(
            env.ref("base.partner_admin").id
        )
        user_admin_id.website = "https://technolibre.ca"
        user_admin_id.name = "Mathieu Benoit"
        user_admin_id.email = "mathieu.benoit@technolibre.ca"
        user_admin_id.country_id = env.ref("base.ca")
        user_admin_id.state_id = env["res.country.state"].search(
            [("code", "ilike", "QC")], limit=1
        )


def post_init_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})

        partner_id = env["res.partner"].browse(env.ref("base.main_company").id)

        partner_img_attachment = env.ref(
            "ore.ir_attachment_logo_ore_transparent_svg"
        )
        with tools.file_open(
            partner_img_attachment.local_url[1:], "rb"
        ) as desc_file:
            image_data = base64.b64encode(desc_file.read())
            partner_id.image = image_data
            # Update favicon web
            env["res.company"].browse(1).favicon = image_data
