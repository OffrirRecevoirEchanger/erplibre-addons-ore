import math

from odoo import _, api, fields, models, tools


class Currency(models.Model):
    _inherit = "res.currency"

    force_decimal_places = fields.Integer(
        default=-1,
        help=(
            "By default, -1, disable. Else ignore compute decimal_places and"
            " use this value."
        ),
    )

    @api.multi
    @api.depends("rounding")
    def _compute_decimal_places(self):
        for currency in self:
            if currency.force_decimal_places != -1:
                currency.decimal_places = currency.force_decimal_places
            else:
                if 0 < currency.rounding < 1:
                    currency.decimal_places = int(
                        math.ceil(math.log10(1 / currency.rounding))
                    )
                else:
                    currency.decimal_places = 0
