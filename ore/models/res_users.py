import logging

from odoo import _, api, exceptions, fields, models

_logger = logging.getLogger(__name__)


class Users(models.Model):
    _inherit = "res.users"

    @api.model_create_multi
    def create(self, vals_list):
        vals = super(Users, self).create(vals_list)
        lst_data = []
        for val in vals:
            existing_adhesion = self.env["ore.demande.adhesion"].search(
                [("courriel", "=", val.email)]
            )
            if existing_adhesion:
                # Force create account
                partner_id = self.env["res.partner"].search(
                    [("email", "=", val.email)]
                )
                # Missing associate with member
                if not partner_id.ore_membre_id:
                    # need to create an account membre
                    value_membre = {"partner_id": partner_id.id}
                    ore_membre_id = self.env["ore.membre"].create(value_membre)
                    # TODO send notification at creation if was invited to a clan
                    existing_adhesion.fill_membre_adhesion(ore_membre_id)
                    existing_adhesion.user_id = val.id
                if existing_adhesion.clan_id:
                    # Create notification
                    value_notif = {
                        "clan_invited_id": existing_adhesion.clan_id.id,
                        "membre_id": partner_id.ore_membre_id.id,
                        "type_notification": "Invitation clan",
                    }
                    notif_id = self.env[
                        "ore.echange.service.notification"
                    ].create(value_notif)
            else:
                data = {
                    "courriel": val.email,
                    "nom": val.name,
                    "telephone": val.phone,
                    "user_id": val.id,
                }
                lst_data.append(data)
        if lst_data:
            self.env["ore.demande.adhesion"].create(lst_data)
        return vals
