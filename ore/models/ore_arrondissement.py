from odoo import _, api, fields, models


class OREArrondissement(models.Model):
    _name = "ore.arrondissement"
    _description = "Ensemble des arrondissement du réseau ORE"
    _rec_name = "nom"

    nom = fields.Char()

    membre = fields.One2many(
        comodel_name="ore.membre",
        inverse_name="arrondissement",
        help="Membre relation",
    )

    ville = fields.Many2one(comodel_name="ore.ville")
