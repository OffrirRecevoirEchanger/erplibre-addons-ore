from odoo import _, api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    type = fields.Selection(selection_add=[("ore", "Temps ORE")])

    ore_temps_valeur_argent = fields.Float(
        default=1, help="La quantité de monnaie pour obtenir 1 heure."
    )
