import logging

from odoo import _, api, exceptions, fields, models

_logger = logging.getLogger(__name__)


class Users(models.Model):
    _inherit = "res.users"

    @api.model_create_multi
    def create(self, vals_list):
        vals = super(Users, self).create(vals_list)
        lst_data = []
        ore_id = self.env["ore.ore"].search([], limit=1)
        for val in vals:
            data = {
                "ore": ore_id.id,
                "courriel": val.email,
                "nom": val.name,
                "telephone": val.phone,
                "user_id": val.id,
            }
            lst_data.append(data)
        if lst_data:
            self.env["ore.demande.adhesion"].create(lst_data)
        return vals
