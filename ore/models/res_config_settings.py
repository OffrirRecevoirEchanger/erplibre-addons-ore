from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    ore_auto_accept_adhesion = fields.Boolean(
        "Auto accept adhesion",
        config_parameter="ore.ore_auto_accept_adhesion",
    )

    ore_default_societe = fields.Many2one(
        string="Default ORE society",
        comodel_name="ore.membre",
        help="Warehouse ORE",
        domain="[('est_un_point_service', '=', True)]",
        config_parameter="ore.ore_default_societe",
    )

    ore_default_free_time = fields.Float(
        string="Default ORE time",
        help="The user receive the default time.",
        config_parameter="ore.ore_default_free_time",
    )
