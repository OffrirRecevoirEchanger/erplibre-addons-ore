from odoo import _, api, fields, models


class ORERegion(models.Model):
    _name = "ore.region"
    _description = "ORE Region"
    _rec_name = "nom"

    nom = fields.Char()

    code = fields.Integer(
        string="Code de région",
        required=True,
        help="Code de la région administrative",
    )

    membre = fields.One2many(
        comodel_name="ore.membre",
        inverse_name="region",
        help="Membre relation",
    )

    ville = fields.One2many(
        comodel_name="ore.ville",
        inverse_name="region",
        help="Ville relation",
    )
