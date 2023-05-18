from odoo import _, api, fields, models


class OREOrigine(models.Model):
    _name = "ore.origine"
    _description = "ORE Origine"
    _rec_name = "nom"

    nom = fields.Char(string="Origine")

    membre = fields.One2many(
        comodel_name="res.partner",
        inverse_name="origine",
        help="Membre relation",
    )
