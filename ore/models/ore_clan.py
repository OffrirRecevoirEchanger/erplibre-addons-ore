import hashlib

from odoo import _, api, fields, models


class OreClan(models.Model):
    _name = "ore.clan"
    _description = "ore_clan"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(track_visibility="onchange")

    active = fields.Boolean(
        string="Actif",
        default=True,
        help=(
            "Lorsque non actif, ce clan n'est plus en fonction,"
            " mais demeure accessible pour consultation historique."
        ),
        track_visibility="onchange",
    )

    # TODO not supported approuve
    approuve = fields.Boolean(
        string="Approuvé",
        help="Permet d'approuver ce clan.",
        track_visibility="onchange",
    )

    description = fields.Text(
        track_visibility="onchange",
    )

    besoin_comble = fields.Text(
        track_visibility="onchange",
    )

    organisation = fields.Char(
        track_visibility="onchange",
    )

    ville_region = fields.Char(
        track_visibility="onchange",
    )

    message_accueil = fields.Char(
        track_visibility="onchange",
    )

    membre_admin_ids = fields.Many2many(
        comodel_name="ore.membre",
        relation="membre_admin_clan_rel",
        string="Membre Admin",
        track_visibility="onchange",
    )

    membre_create_id = fields.Many2one(
        comodel_name="ore.membre",
        string="Membre Create",
        track_visibility="onchange",
    )

    membre_list_ids = fields.Many2many(
        comodel_name="ore.membre",
        string="Membre",
        relation="membre_clan_participe_rel",
        track_visibility="onchange",
    )

    invitation_by_admin_ids = fields.One2many(
        comodel_name="ore.clan.invitation",
        string="Invitation par admin",
        inverse_name="clan_id",
        domain=[("invite_by_admin_clan", "=", True)],
        track_visibility="onchange",
    )

    invitation_asked_ids = fields.One2many(
        comodel_name="ore.clan.invitation",
        string="Invitation demandé",
        inverse_name="clan_id",
        domain=[("ask_join_clan", "=", True)],
        track_visibility="onchange",
    )

    image = fields.Binary(
        "Image",
        attachment=True,
        help=(
            "This field holds the image used as avatar for this contact,"
            " limited to 1024x1024px"
        ),
        track_visibility="onchange",
    )

    valeur_clan = fields.Text(
        track_visibility="onchange",
    )

    membre_list_count = fields.Integer(
        string="Membre count",
        compute="_compute_membre_list_count",
        store=True,
        track_visibility="onchange",
    )

    website_published = fields.Boolean(
        string="Clan rendu public",
        default=True,
        help="Le clan est publiée, sinon il est privée.",
        track_visibility="onchange",
    )

    @api.depends("membre_list_ids")
    def _compute_membre_list_count(self):
        for rec in self:
            rec.membre_list_count = len(rec.membre_list_ids)

    def website_publish_button(self):
        self.ensure_one()
        return self.write({"website_published": not self.website_published})

    @api.model_create_multi
    def create(self, vals_list):
        vals = super().create(vals_list)
        for val in vals:
            # Automatic message accueil
            msg_bienvenu = f"Bienvenue dans le clan {val.name}"
            if not val.message_accueil:
                val.message_accueil = msg_bienvenu
            # Force create char clan
            chat_group_ids = self.env["ore.chat.group"].search(
                [("clan_id", "=", val.id)]
            )
            if not chat_group_ids:
                chat_group_value = {
                    "clan_id": val.id,
                    # "membre_ids": val.membre_list_ids.ids,
                }
                chat_group_id = self.env["ore.chat.group"].create(
                    chat_group_value
                )
                chat_msg_value = {
                    "membre_writer_id": val.membre_create_id.id,
                    "name": msg_bienvenu,
                    "msg_group_id": chat_group_id.id,
                }
                self.env["ore.chat.message"].create(chat_msg_value)
                # notify
                # Create notification
                value_notif = {
                    "clan_new_id": val.id,
                    # "date_created": val.create_date,
                    "membre_id": val.membre_create_id.id,
                    "broadcast_public": True,
                    "type_notification": "Clan creation",
                }
                notif_id = self.env["ore.echange.service.notification"].create(
                    value_notif
                )
        return vals

    @api.multi
    def write(self, vals):
        status = super().write(vals)
        if "membre_list_ids" in vals.keys():
            # Because we change the list, just check everything is fine
            for rec in self:
                for membre_id in rec.membre_list_ids:
                    if not membre_id.clan_principal_id:
                        # Force update clan principal
                        # TODO support to remove clan principal
                        membre_id.clan_principal_id = rec.id
        return status

    def get_image_url(self, field="image"):
        # field can be image_medium or image_small
        # website_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        # unique = self.write_date.strftime('%Y%m%d%H%M%S')
        # url = f"{website_url}/web/image?model=res.partner&id={self.partner_id.id}&field={field}&unique={unique}"
        # return url
        return self.image_url(self, field)

    @api.model
    def image_url(self, record, field, size=None):
        """Returns a local url that points to the image field of a given browse record."""
        sudo_record = record.sudo()
        sha = hashlib.sha1(
            str(getattr(sudo_record, "__last_update")).encode("utf-8")
        ).hexdigest()[0:7]
        size = "" if size is None else "/%s" % size
        return "/web/image/%s/%s/%s%s?unique=%s" % (
            record._name,
            record.id,
            field,
            size,
            sha,
        )
