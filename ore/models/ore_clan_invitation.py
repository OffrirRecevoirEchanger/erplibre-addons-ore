from collections import defaultdict

from odoo import _, api, fields, models


class OreClanInvitation(models.Model):
    _name = "ore.clan.invitation"
    _description = "Invitation to a clan"
    _rec_name = "email"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    email = fields.Char(
        track_visibility="onchange",
    )

    active = fields.Boolean(
        string="Actif",
        default=True,
        help=(
            "Lorsque non actif, cette invitation n'est plus en fonction,"
            " mais demeure accessible pour consultation historique."
        ),
        track_visibility="onchange",
    )

    clan_id = fields.Many2one(
        comodel_name="ore.clan",
        string="Clan",
        track_visibility="onchange",
        required=True,
    )

    invite_by_admin_clan = fields.Boolean(
        string="Invite by admin clan",
        track_visibility="onchange",
    )

    ask_join_clan = fields.Boolean(
        string="Ask join clan",
        track_visibility="onchange",
    )

    stage_id = fields.Many2one(
        comodel_name="ore.clan.invitation.stage",
        string="Stage",
        default=lambda s: s._default_stage_id(),
        track_visibility="onchange",
    )

    def _default_stage_id(self):
        return self.env["ore.clan.invitation.stage"].search(
            [], order="sequence asc", limit=1
        )

    @api.model_create_multi
    def create(self, vals_list):
        vals = super().create(vals_list)
        # Create notification
        for rec in vals:
            partner_ids = self.env["res.partner"].search(
                [("email", "=", rec.email)]
            )
            membre_ids = self.env["ore.membre"].search(
                [("partner_id", "in", partner_ids.ids)]
            )
            for membre_id in membre_ids:
                if rec.ask_join_clan:
                    for admin_id in rec.clan_id.membre_admin_ids:
                        value_notif = {
                            "clan_invited_id": rec.clan_id.id,
                            "membre_id": admin_id.id,
                            "membre_from_id": membre_id.id,
                            "type_notification": "Demande adhésion clan",
                        }
                        notif_id = self.env[
                            "ore.echange.service.notification"
                        ].create(value_notif)
                if rec.invite_by_admin_clan:
                    value_notif = {
                        "clan_invited_id": rec.clan_id.id,
                        "membre_id": membre_id.id,
                        "type_notification": "Invitation clan",
                    }
                    notif_id = self.env[
                        "ore.echange.service.notification"
                    ].create(value_notif)
        return vals

    @api.multi
    def write(self, vals):
        res = super().write(vals)
        dct_notification = defaultdict(list)
        for rec in self:
            membre_list_ids = rec.clan_id.membre_list_ids
            partner_ids = self.env["res.partner"].search(
                [("email", "=", rec.email)]
            )
            membre_ids = self.env["ore.membre"].search(
                [("partner_id", "in", partner_ids.ids)]
            )
            lst_membre_list_edit = []
            for membre_id in membre_ids:
                is_refuse = False
                if "stage_id" in vals.keys():
                    if rec.stage_id in (
                        self.env.ref("ore.ore_clan_invitation_stage_refuse"),
                    ):
                        is_refuse = True
                    if rec.stage_id in (
                        self.env.ref("ore.ore_clan_invitation_stage_init"),
                        self.env.ref("ore.ore_clan_invitation_stage_refuse"),
                    ):
                        if membre_id in membre_list_ids:
                            lst_membre_list_edit.append((3, membre_id.id))
                            if is_refuse:
                                dct_notification["refuse"].append(membre_id.id)
                    elif rec.stage_id == self.env.ref(
                        "ore.ore_clan_invitation_stage_approuve"
                    ):
                        if membre_id not in membre_list_ids:
                            lst_membre_list_edit.append((4, membre_id.id))
                            dct_notification["accept"].append(membre_id.id)
            for status_str, lst_membre in dct_notification.items():
                for id_membre_id in lst_membre:
                    # Notification
                    notif_exist_id = self.env[
                        "ore.echange.service.notification"
                    ].search(
                        [
                            ("clan_invited_id", "=", rec.clan_id.id),
                            ("membre_id", "=", id_membre_id),
                        ]
                    )
                    if not notif_exist_id:
                        if rec.active:
                            type_notification = (
                                "Demande adhésion clan accepté"
                                if status_str == "accept"
                                else "Demande adhésion clan refusé"
                            )
                            value_notif = {
                                "clan_invited_id": rec.clan_id.id,
                                "membre_id": id_membre_id,
                                # "date_created": rec.create_date,
                                "type_notification": type_notification,
                            }
                            notif_id = self.env[
                                "ore.echange.service.notification"
                            ].create(value_notif)
                    else:
                        # TODO update it
                        # TODO enlever la notification s'il a été accepté, quand le stage est rendu à approuve ou refusé
                        pass
                        # print("update")
                    # print("ok")
                # value_notif = {
                #     "clan_invited_id": rec.clan_id.id,
                #     "membre_id": membre_id.id,
                #     "date_created": rec.create_date,
                #     "type_notification": "Invitation clan",
                # }
                # notif_id = self.env[
                #     "ore.echange.service.notification"
                # ].create(value_notif)
            if lst_membre_list_edit:
                rec.clan_id.membre_list_ids = lst_membre_list_edit
                # TODO mettre les clan par défaut si c'est son premier clan, devrait être mis dans la gestion du membre au write
        return res
