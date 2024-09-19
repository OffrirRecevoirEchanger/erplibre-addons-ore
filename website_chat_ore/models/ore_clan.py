from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class OREClan(models.Model):
    _inherit = ["ore.clan"]

    @api.multi
    def write(self, vals):
        status = super().write(vals)

        # Detect user
        if "membre_list_ids" in vals:
            for rec in self:
                # We know the list of member has update, check if all members has principal clan
                chat_group_id = self.env["ore.chat.group"].search(
                    [("clan_id", "=", rec.id)], limit=1
                )
                for membre_id in rec.membre_list_ids:
                    # Validate clan principal is set
                    if not membre_id.clan_principal_id:
                        membre_id.clan_principal_id = rec.id
                    # Force to add into clan chat
                    if membre_id.id not in chat_group_id.membre_ids.ids:
                        chat_group_id.membre_ids = [(4, membre_id.id)]
        return status
