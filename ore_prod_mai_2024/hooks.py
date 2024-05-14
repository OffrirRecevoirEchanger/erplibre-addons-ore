import os

from odoo import SUPERUSER_ID, _, api, fields, models


def post_init_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})

        website_ids = env["website"].search([])
        website_ids.domain = "127.0.0.1:8069"
        website_value = {
            "name": "Trouve ton clan",
            "domain": "localhost:8069",
            "auth_signup_uninvited": "b2c",
            "salesteam_id": website_ids.salesteam_id.id,
            "theme_id": website_ids.theme_id.id,
        }
        website_id = env["website"].create(website_value)
        website_ids.cart_recovery_mail_template_id = (
            website_id.cart_recovery_mail_template_id.id
        )
        print("End installation ore_prod_mai_2024")
