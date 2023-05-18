from odoo import _, api, fields, models


class ORETypeCommunication(models.Model):
    _name = "ore.type.communication"
    _description = "ORE Type Communication"
    _rec_name = "nom"

    nom = fields.Char(string="Typecommunication")

    membre = fields.One2many(
        comodel_name="res.partner",
        inverse_name="type_communication",
        help="Membre relation",
    )
