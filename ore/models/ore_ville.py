from odoo import _, api, fields, models


class OREVille(models.Model):
    _name = "ore.ville"
    _description = "ORE Ville"
    _rec_name = "nom"

    nom = fields.Char()

    arrondissement = fields.One2many(
        comodel_name="ore.arrondissement",
        inverse_name="ville",
        help="Arrondissement relation",
    )

    code = fields.Integer(
        required=True,
        help="Code de la ville",
    )

    membre = fields.One2many(
        comodel_name="res.partner",
        inverse_name="ville",
        help="Membre relation",
    )

    region = fields.Many2one(
        comodel_name="ore.region",
        string="Région",
    )
