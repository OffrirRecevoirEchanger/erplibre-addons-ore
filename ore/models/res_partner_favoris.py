from datetime import datetime

from odoo import _, api, fields, models


class ResPartner(models.Model):
    _name = "res.partner.favoris"
    _description = "ORE Membre Favoris des membres"
    _rec_name = "membre_id"

    membre_id = fields.Many2one(
        comodel_name="res.partner",
        string="Membre",
    )
