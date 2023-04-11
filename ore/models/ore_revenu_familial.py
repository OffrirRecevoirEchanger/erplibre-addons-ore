from odoo import _, api, fields, models


class ORERevenuFamilial(models.Model):
    _name = "ore.revenu.familial"
    _description = "ORE Revenu Familial"
    _rec_name = "nom"

    nom = fields.Char(string="Revenu")

    membre = fields.One2many(
        comodel_name="ore.membre",
        inverse_name="revenu_familial",
        help="Membre relation",
    )
