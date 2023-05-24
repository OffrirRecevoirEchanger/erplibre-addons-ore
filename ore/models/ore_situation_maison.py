from odoo import _, api, fields, models


class ORESituationMaison(models.Model):
    _name = "ore.situation.maison"
    _description = "ORE Situation Maison"
    _rec_name = "nom"

    nom = fields.Char(string="Situation")

    membre = fields.One2many(
        comodel_name="ore.membre",
        inverse_name="situation_maison",
        help="Membre relation",
    )
