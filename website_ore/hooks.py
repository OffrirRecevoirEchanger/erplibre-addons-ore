# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64

from odoo import SUPERUSER_ID, _, api, fields, models, tools


def pre_init_hook(cr):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        # Remove all website pages before installing data

        website_page_ids = env["website.page"].search([])
        website_menu_ids = env["website.menu"].search([])
        # TODO website doesn't support multi
        # website_page_ids.website_id = None
        # TODO replace by :
        for website_page in website_page_ids:
            website_page.website_id = None
        for website_menu in website_menu_ids:
            website_menu.website_id = None


def post_init_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        website_page = env["website.page"].browse(
            env.ref("website_ore.website_page_home").id
        )
        # Update website favicon
        favicon_img_attachment = env.ref(
            "ore.ir_attachment_logo_ore_transparent_svg"
        )
        with tools.file_open(
            favicon_img_attachment.local_url[1:], "rb"
        ) as desc_file:
            website_page.website_id.favicon = base64.b64encode(
                desc_file.read()
            )
