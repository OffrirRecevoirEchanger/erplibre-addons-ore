from odoo import _, api, fields, models


class OREPointService(models.Model):
    _name = "ore.point.service"
    _description = "ORE Point Service"
    _rec_name = "nom"

    nom = fields.Char(help="Nom du point de service")

    ore = fields.Many2one(
        string="Réseau",
        comodel_name="ore.ore",
        required=True,
    )

    commentaire = fields.One2many(
        comodel_name="ore.commentaire",
        inverse_name="point_service",
        help="Commentaire relation",
    )

    membre = fields.One2many(
        comodel_name="ore.membre",
        inverse_name="point_service",
        help="Membre relation",
    )

    sequence = fields.Integer(
        string="Séquence",
        help="Séquence d'affichage",
    )
