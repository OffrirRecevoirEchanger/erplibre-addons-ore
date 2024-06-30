import logging
import uuid

from odoo import _, api, fields, models

try:
    import email_validator
except ImportError:
    email_validator = None

_logger = logging.getLogger(__name__)


class OREDemandeAdhesion(models.Model):
    _name = "ore.demande.adhesion"
    _description = "ORE Demande Adhesion"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "nom_complet"

    nom_complet = fields.Char(
        string="Nom complet",
        compute="_compute_nom_complet",
        store=True,
        track_visibility="onchange",
    )

    active = fields.Boolean(
        string="Actif",
        default=True,
        help=(
            "Lorsque non actif, cet demande d'adhésion n'est plus en fonction,"
            " mais demeure accessible."
        ),
        track_visibility="onchange",
    )

    courriel = fields.Char(
        track_visibility="onchange",
    )

    date_mise_a_jour = fields.Datetime(
        string="Dernière mise à jour",
        help="Date de la dernière mise à jour",
        track_visibility="onchange",
    )

    en_attente = fields.Boolean(
        string="En attente",
        default=True,
        track_visibility="onchange",
    )

    nom = fields.Char(
        track_visibility="onchange",
    )

    poste = fields.Char(
        track_visibility="onchange",
    )

    prenom = fields.Char(
        string="Prénom",
        track_visibility="onchange",
    )

    telephone = fields.Char(
        string="Téléphone",
        track_visibility="onchange",
    )

    transferer = fields.Boolean(
        string="Transféré",
        track_visibility="onchange",
    )

    only_invitation = fields.Boolean(
        string="Seulement invitation par courriel",
        help="Ne va pas créer de compte utilisateur.",
        track_visibility="onchange",
    )

    clan_id = fields.Many2one(
        comodel_name="ore.clan",
        string="Clan associé",
        track_visibility="onchange",
    )

    invitation_from_membre_id = fields.Many2one(
        comodel_name="ore.membre",
        string="Invité par membre",
        track_visibility="onchange",
    )

    user_id = fields.Many2one(
        comodel_name="res.users",
        string="User",
        track_visibility="onchange",
    )

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.user.company_id,
        help=(
            "If set, directories and files will only be available for the"
            " selected company."
        ),
        track_visibility="onchange",
    )

    url_invitation_redirect = fields.Char(
        help="Will be the url send to user by email.",
        track_visibility="onchange",
    )

    company_website_id = fields.Many2one(
        comodel_name="website",
        string="website",
        help="Will be use for email invitation.",
        track_visibility="onchange",
    )

    @api.depends("nom", "prenom")
    def _compute_nom_complet(self):
        for rec in self:
            if rec.nom and rec.prenom:
                rec.nom_complet = f"{rec.prenom} {rec.nom}"
            elif rec.nom:
                rec.nom_complet = f"{rec.nom}"
            elif rec.prenom:
                rec.nom_complet = f"{rec.prenom}"
            else:
                rec.nom_complet = False

    @api.model_create_multi
    def create(self, vals_list):
        vals = super(OREDemandeAdhesion, self).create(vals_list)
        for rec in vals:
            if rec.only_invitation:
                continue
            rec.fill_membre_adhesion(membre_id=None)
        return vals

    def fill_membre_adhesion(self, membre_id=None):
        auto_approuve = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("ore.ore_auto_accept_adhesion")
        )
        default_ore_society = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("ore.ore_default_societe")
        )
        default_free_time = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("ore.ore_default_free_time", 0)
        )
        if default_ore_society:
            society_id = self.env["ore.membre"].browse(
                int(default_ore_society)
            )
        else:
            society_id = None
        for rec in self:
            if not membre_id:
                data = {
                    "profil_approuver": auto_approuve,
                    "name": rec.nom_complet,
                    # "parent_id": self.env.ref("base.main_partner").id,
                    # "reseau_ore_id": society_id.id,
                    "user_id": rec.user_id.id,
                    "partner_id": rec.user_id.partner_id.id,
                    "ore_client_key": uuid.uuid4().hex,
                }
                if society_id:
                    data["region"] = society_id.region.id
                    data["ville"] = society_id.ville.id

                if rec.clan_id:
                    data["clan_principal_id"] = rec.clan_id.id
                    data["clan_participe_ids"] = [(6, 0, rec.clan_id.id)]

                membre_id = self.env["ore.membre"].create(data)
            else:
                membre_id.profil_approuver = auto_approuve
                if not membre_id.ore_client_key:
                    membre_id.ore_client_key = uuid.uuid4().hex
                if rec.user_id:
                    membre_id.user_id = rec.user_id.id
                    if not membre_id.partner_id:
                        membre_id.partner_id = rec.user_id.partner_id.id

            # Force add initial time
            if default_free_time:
                data_service_time = {
                    "date_echange": fields.Datetime.now(),
                    "nb_heure": float(default_free_time),
                    "type_echange": "offre_ponctuel",
                    "transaction_valide": True,
                    "membre_acheteur": society_id.id,
                    "membre_vendeur": membre_id.id,
                }
                self.env["ore.echange.service"].create(data_service_time)

    @staticmethod
    def validate_email(email):
        try:
            email_info = email_validator.validate_email(
                email, check_deliverability=False
            )
            return True, email_info.normalized
        except email_validator.EmailNotValidError as e:
            return False, str(e)

    def send_invitation_per_email_to_adhesion(self):
        for rec in self:
            default_website = (
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("ore.ore_default_website_invitation_adhesion")
            )
            if default_website:
                default_website = int(default_website)
            else:
                default_website = self.env.ref("website.default_website").id
            rec.company_website_id = default_website
            rec.url_invitation_redirect = (
                f"http://{rec.company_website_id.domain}/ore/ore_clan/%s"
                % rec.clan_id.id
            )
            mail_id_i = (
                self.env.ref("ore.ore_invite_adhesion_to_clan")
                .sudo()
                .send_mail(rec.id, force_send=True)
            )
            _logger.info(
                "Send invitation email adhesion to clan for email"
                f" {rec.courriel} from user email"
                f" {rec.invitation_from_membre_id.email}. Mail id {mail_id_i}"
            )
