from odoo import _, api, fields, models


class OREInteret(models.Model):
    _name = "ore.membre.interet"
    _description = "ORE Membre Interet des membres"

    name = fields.Char(string="interet")
