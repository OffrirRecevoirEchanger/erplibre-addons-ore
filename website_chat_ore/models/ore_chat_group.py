import logging
from datetime import datetime

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class OREChatGroup(models.Model):
    _name = "ore.chat.group"
    _description = "ORE chat group"

    name = fields.Char(
        compute="_compute_name",
        store=True,
        track_visibility="onchange",
    )

    active = fields.Boolean(default=True)

    membre_ids = fields.Many2many(
        comodel_name="ore.membre",
        string="Membres",
        help="Membres du groupe.",
    )

    msg_ids = fields.One2many(
        comodel_name="ore.chat.message",
        string="Messages",
        inverse_name="msg_group_id",
    )

    clan_id = fields.Many2one(
        comodel_name="ore.clan",
        string="Clan",
    )

    group_clan_id = fields.Many2one(
        comodel_name="ore.clan.group",
        string="Group Clan",
    )

    @api.depends("membre_ids", "clan_id")
    def _compute_name(self):
        for rec in self:
            if rec.clan_id:
                rec.name = rec.clan_id.name
            elif rec.membre_ids:
                rec.name = " - ".join([a.name for a in rec.membre_ids])
            else:
                rec.name = "Empty"

    def first_to_json(self, actual_membre_id=None):
        obj = self[0]
        if actual_membre_id:
            lst_other_membre_id = [
                a for a in obj.membre_ids if a.id != actual_membre_id
            ]
        else:
            lst_other_membre_id = []
        if not obj.membre_ids and not obj.clan_id:
            _logger.warning("Why members is empty?")
            data = {}
        else:
            if actual_membre_id:
                if lst_other_membre_id:
                    other_membre_id = lst_other_membre_id[0]
                else:
                    # Same member
                    other_membre_id = obj.membre_ids[0]
            last_msg = obj.msg_ids[-1].name if obj.msg_ids else ""
            if obj.clan_id:
                name = obj.clan_id.name
            elif not actual_membre_id:
                name = other_membre_id.name
            else:
                name = ""
            data = {
                # "id": obj.id,
                "id_group": obj.id,
                "name": name,
                "resume_msg": last_msg,
                "lst_msg": [a.first_to_json() for a in obj.msg_ids],
            }
            if obj.clan_id:
                data["clan_id"] = obj.clan_id.id
            if obj.group_clan_id:
                data["group_clan_id"] = obj.group_clan_id.id
            if actual_membre_id:
                data["ma_photo"] = other_membre_id.get_image_url()
                data["id"] = other_membre_id.id
            elif obj.clan_id:
                data["ma_photo"] = obj.clan_id.get_image_url()
        return data
