from odoo import _, api, fields, models


class ORELangueParle(models.Model):
    _name = "ore.membre.langue_parle"
    _description = "ORE Membre Langue des membres"

    name = fields.Char(string="langue_parle")
