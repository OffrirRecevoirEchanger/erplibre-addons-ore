from odoo import _, api, fields, models


class OREProvenance(models.Model):
    _name = "ore.provenance"
    _description = "ORE Provenance"
    _rec_name = "nom"

    nom = fields.Char(string="Provenance")

    membre = fields.One2many(
        comodel_name="ore.membre",
        inverse_name="provenance",
        help="Membre relation",
    )
