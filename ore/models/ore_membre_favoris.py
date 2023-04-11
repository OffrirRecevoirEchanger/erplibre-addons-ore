from datetime import datetime

from odoo import _, api, fields, models


class OREMembre(models.Model):
    _name = "ore.membre.favoris"
    _description = "ORE Membre Favoris des membres"
    _rec_name = "membre_id"

    membre_id = fields.Many2one(
        comodel_name="ore.membre",
        string="Membre",
    )
