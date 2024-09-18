import logging
from datetime import datetime

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class OREEchangeServiceNotification(models.Model):
    _name = "ore.echange.service.notification"
    _description = "ORE Echange Service Notification"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc"

    name = fields.Char(
        compute="_compute_name",
        store=True,
        track_visibility="onchange",
    )

    active = fields.Boolean(
        default=True,
        track_visibility="onchange",
    )

    is_read = fields.Boolean(
        string="Is read",
        help="La notification a été lu par le membre.",
        track_visibility="onchange",
    )

    type_notification = fields.Selection(
        selection=[
            ("Nouvelle demande de service", "Nouvelle demande de service"),
            ("Réponse à votre demande", "Réponse à votre demande"),
            ("Demande de service", "Demande de service"),
            ("Proposition de service", "Proposition de service"),
            # ("Réponse à votre offre", "Réponse à votre offre"),
            ("Transaction validée", "Transaction validée"),
            ("Invitation clan", "Invitation clan"),
            ("Clan creation", "Création d'un nouveau clan"),
        ],
        track_visibility="onchange",
    )

    echange_service_id = fields.Many2one(
        comodel_name="ore.echange.service",
        string="Échange de service",
        track_visibility="onchange",
    )

    membre_id = fields.Many2one(
        comodel_name="ore.membre",
        string="Membre notifié",
        track_visibility="onchange",
    )

    broadcast_membre = fields.Boolean(
        help="If True, will send message for all member"
    )

    broadcast_public = fields.Boolean(
        help="If True, will send message for all public"
    )

    membre_name = fields.Char(
        compute="_compute_membre_name",
        store=True,
        track_visibility="onchange",
    )

    membre_logo = fields.Char(
        compute="_compute_name",
        store=True,
        track_visibility="onchange",
    )

    clan_invited_id = fields.Many2one(
        comodel_name="ore.clan",
        string="Invitation au clan",
        track_visibility="onchange",
    )

    clan_new_id = fields.Many2one(
        comodel_name="ore.clan",
        string="Nouveau clan",
        track_visibility="onchange",
    )

    def first_to_json(self):
        obj = self[0]
        data = {
            "id": obj.id,
            "name": obj.name,
            "is_read": obj.is_read,
            "type_notification": obj.type_notification,
            "echange_service_id": obj.echange_service_id.id,
            "membre_id": obj.membre_id.id,
            "membre_name": obj.membre_name,
            "membre_photo": obj.membre_logo,
            "clan_invited_id": obj.clan_invited_id.id,
            "clan_new_id": obj.clan_new_id.id,
        }
        return data

    @api.depends(
        "echange_service_id", "membre_id", "clan_invited_id", "clan_new_id"
    )
    def _compute_name(self):
        for rec in self:
            lst_msg = []
            if (
                rec.echange_service_id.membre_acheteur
                and rec.echange_service_id.membre_acheteur.id
                != rec.membre_id.id
            ):
                lst_msg.append(
                    f"Membre : '{rec.echange_service_id.membre_acheteur.name}'"
                )
                rec.membre_logo = (
                    rec.echange_service_id.membre_acheteur.get_image_url()
                )
            if (
                rec.echange_service_id.membre_vendeur
                and rec.echange_service_id.membre_vendeur.id
                != rec.membre_id.id
            ):
                lst_msg.append(
                    f"Membre : '{rec.echange_service_id.membre_vendeur.name}'"
                )
                rec.membre_logo = (
                    rec.echange_service_id.membre_vendeur.get_image_url()
                )
            if rec.echange_service_id.offre_service:
                lst_msg.append(
                    f"Offre : '{rec.echange_service_id.offre_service.titre}'"
                )
            if rec.echange_service_id.demande_service:
                lst_msg.append(
                    "Demande :"
                    f" '{rec.echange_service_id.demande_service.titre}'"
                )
            if rec.clan_invited_id:
                lst_msg.append(
                    f"Invitation au clan : '{rec.clan_invited_id.name}'"
                )
                rec.membre_logo = rec.clan_invited_id.get_image_url()
            if rec.clan_new_id:
                lst_msg.append(rec.clan_new_id.name)
                rec.membre_logo = rec.clan_new_id.get_image_url()
            rec.name = " - ".join(lst_msg)

    @api.depends("membre_id")
    def _compute_membre_name(self):
        for rec in self:
            rec.membre_name = rec.membre_id.name if rec.membre_id else ""

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for rec in res:
            data = rec.first_to_json()
            if rec.broadcast_public:
                canal = f'["{rec.type_notification}","PUBLIC"]'
            elif rec.broadcast_membre:
                # TODO not supported
                canal = f'["{self._cr.dbname}","{self._name}","MEMBRE"]'
            elif rec.membre_id:
                canal = (
                    f'["{self._cr.dbname}","{self._name}",{rec.membre_id.id}]'
                )
            else:
                _logger.error(
                    f"Cannot send notification id '{rec.id}' name '{rec.name}'"
                    " because missing membre_id or broadcast option."
                )
                continue
            self.env["bus.bus"].sendone(
                # f'["{self._cr.dbname}","{self._name}",{rec.id}]',
                "ore.notification.echange",
                {
                    "timestamp": str(datetime.now()),
                    "data": data,
                    "field_id": rec.id,
                    "canal": canal,
                },
            )
        return res

    @api.multi
    def write(self, vals):
        res = super().write(vals)
        for rec in self:
            data = rec.first_to_json()
            self.env["bus.bus"].sendone(
                # f'["{self._cr.dbname}","{self._name}",{rec.id}]',
                "ore.notification.echange",
                {
                    "timestamp": str(datetime.now()),
                    "data": data,
                    "field_id": rec.id,
                    "canal": f'["{self._cr.dbname}","{self._name}","UPDATE",{rec.membre_id.id}]',
                },
            )
        return res
