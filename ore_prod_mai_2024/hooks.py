import os

from odoo import SUPERUSER_ID, _, api, fields, models


def post_init_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})

        website_first_id = env.ref("website.default_website")
        website_first_id.domain = "127.0.0.1:8069"
        website_id = env.ref("website_ore.trouve_ton_clan_website")
        website_id.salesteam_id = website_first_id.salesteam_id.id
        website_id.theme_id = website_first_id.theme_id.id
        website_id.domain = "localhost:8069"
        website_first_id.cart_recovery_mail_template_id = (
            website_id.cart_recovery_mail_template_id.id
        )
        # Delete create by default
        website_page_ids = env["website.page"].search(
            [("website_id", "=", website_id.id)], order="view_id desc", limit=1
        )
        website_page_ids.unlink()

        print("End installation ore_prod_mai_2024")
