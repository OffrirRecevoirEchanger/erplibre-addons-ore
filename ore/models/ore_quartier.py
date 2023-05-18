from odoo import _, api, fields, models


class OREQuartier(models.Model):
    _name = "ore.quartier"
    _description = "ORE Quartier"
    _rec_name = "nom"

    nom = fields.Char(
        string="Nom du quartier",
        help="Nom du quartier",
    )

    arrondissement = fields.Many2one(
        comodel_name="ore.arrondissement",
        required=True,
        help="Arrondissement associé au quartier",
    )

    membre = fields.One2many(
        comodel_name="res.partner",
        inverse_name="quartier",
        help="Membre relation",
    )
