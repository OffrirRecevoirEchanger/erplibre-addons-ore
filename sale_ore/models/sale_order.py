from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"
    _description = "sale_order"

    ore_client_key = fields.Char(related="partner_id.ore_client_key")

    currency_ORE_id = fields.Many2one(
        "res.currency",
        string="ORE Currency",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        default=lambda self: self.env.ref(
            "sale_ore.ORE", raise_if_not_found=False
        ),
        track_visibility="always",
    )

    amount_ore_temps_effectue = fields.Monetary(
        store=True,
        currency_field="currency_ORE_id",
        readonly=True,
        compute="_amount_ore_all",
        track_visibility="always",
        help="Temps HH:MM en liaison avec un client ORE.",
    )

    manual_add_ore_temps_effectue = fields.Monetary(
        currency_field="currency_ORE_id",
        track_visibility="always",
        help="Temps supplémentaires HH:MM en liaison avec un client ORE.",
    )

    @api.depends("order_line.price_total", "manual_add_ore_temps_effectue")
    def _amount_ore_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            # TODO missing conversion currency to time
            sum_temps = (
                sum(
                    [
                        abs(
                            a.price_subtotal
                            / a.product_id.ore_temps_valeur_argent
                        )
                        if a.product_id.ore_temps_valeur_argent
                        else 0
                        for a in order.order_line
                        if a.product_id.type == "ore"
                    ]
                )
                + order.manual_add_ore_temps_effectue
            )

            order.amount_ore_temps_effectue = order.currency_ORE_id.round(
                sum_temps
            )
