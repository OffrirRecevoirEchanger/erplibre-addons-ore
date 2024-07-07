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
    )

    invite_by_admin_clan = fields.Boolean(
        string="Invite by admin clan",
        track_visibility="onchange",
    )

    ask_join_clan = fields.Boolean(
        string="Ask join clan",
        track_visibility="onchange",
    )
