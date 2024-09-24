from odoo import _, api, fields, models


class OreNotificationChat(models.Model):
    _name = "ore.notification.chat"
    _description = "ore_notification_chat"

    name = fields.Char(
        compute="_compute_name",
        store=True,
        track_visibility="onchange",
    )

    group_id = fields.Many2one(
        comodel_name="ore.chat.group",
        string="Group",
        required=True,
    )

    is_read = fields.Boolean()

    membre_notify_id = fields.Many2one(
        comodel_name="ore.membre",
        string="Membre Notify",
        required=True,
    )

    @api.depends("membre_notify_id", "group_id")
    def _compute_name(self):
        for rec in self:
            rec.name = (
                f"Group '{rec.group_id.name}' membre"
                f" '{rec.membre_notify_id.name}'"
            )
