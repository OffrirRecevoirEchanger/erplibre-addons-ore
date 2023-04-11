from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    ore_auto_accept_adhesion = fields.Boolean(
        "Auto accept adhesion",
        config_parameter="ore.ore_auto_accept_adhesion",
    )
