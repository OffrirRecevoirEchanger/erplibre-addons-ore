import os

from odoo import SUPERUSER_ID, _, api, fields, models


def post_init_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})

        website_first_id = env.ref("website.default_website")
        website_first_id.domain = "127.0.0.1:8069"
        website_id = env.ref("website_ore.trouve_ton_clan_website")
        website_id.domain = "localhost:8069"

        custom_muk_web_theme_id = env["ir.ui.view"].search(
            [
                (
                    "name",
                    "=",
                    "/muk_web_theme/static/src/scss/colors.custom.muk_web_theme._assets_primary_variables.scss",
                )
            ]
        )
        custom_muk_web_theme_id.unlink()

        print("End installation ore_prod_jul_2024")
