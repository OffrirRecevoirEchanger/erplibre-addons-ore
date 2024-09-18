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
        return vals

    @api.multi
    def write(self, vals):
        res = super().write(vals)
        if "stage_id" in vals.keys():
            for rec in self:
                membre_list_ids = rec.clan_id.membre_list_ids
                partner_ids = self.env["res.partner"].search(
                    [("email", "=", rec.email)]
                )
                membre_ids = self.env["ore.membre"].search(
                    [("partner_id", "in", partner_ids.ids)]
                )
                lst_membre_list_edit = []
                if rec.stage_id in (
                    self.env.ref("ore.ore_clan_invitation_stage_init"),
                    self.env.ref("ore.ore_clan_invitation_stage_refuse"),
                ):
                    for membre_id in membre_ids:
                        if membre_id in membre_list_ids:
                            lst_membre_list_edit.append((3, membre_id.id))
                elif rec.stage_id == self.env.ref(
                    "ore.ore_clan_invitation_stage_approuve"
                ):
                    for membre_id in membre_ids:
                        if membre_id not in membre_list_ids:
                            lst_membre_list_edit.append((4, membre_id.id))
                if lst_membre_list_edit:
                    rec.clan_id.membre_list_ids = lst_membre_list_edit
                # TODO notification
        return res
