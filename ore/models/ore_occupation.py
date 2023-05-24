from odoo import _, api, fields, models


class OREOccupation(models.Model):
    _name = "ore.occupation"
    _description = "ORE Occupation"
    _rec_name = "nom"

    nom = fields.Char(string="Occupation")

    membre = fields.One2many(
        comodel_name="ore.membre",
        inverse_name="occupation",
        help="Membre relation",
    )
