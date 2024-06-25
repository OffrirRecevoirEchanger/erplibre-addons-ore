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
    _rec_name = "nom_complet"

    nom_complet = fields.Char(
        string="Nom complet",
        compute="_compute_nom_complet",
        store=True,
    )

    active = fields.Boolean(
        string="Actif",
        default=True,
        help=(
            "Lorsque non actif, cet demande d'adhésion n'est plus en fonction,"
            " mais demeure accessible."
        ),
    )

    courriel = fields.Char()

    date_mise_a_jour = fields.Datetime(
        string="Dernière mise à jour",
        help="Date de la dernière mise à jour",
    )

    en_attente = fields.Boolean(
        string="En attente",
        default=True,
    )

    nom = fields.Char()

    poste = fields.Char()

    prenom = fields.Char(string="Prénom")

    telephone = fields.Char(string="Téléphone")

    transferer = fields.Boolean(string="Transféré")

    only_invitation = fields.Boolean(
        string="Seulement invitation par courriel",
        help="Ne va pas créer de compte utilisateur.",
    )

    clan_id = fields.Many2one(comodel_name="ore.clan", string="Clan associé")

    invitation_from_membre_id = fields.Many2one(
        comodel_name="ore.membre", string="Invité par membre"
    )

    user_id = fields.Many2one(
        comodel_name="res.users",
        string="User",
    )

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.user.company_id,
        help=(
            "If set, directories and files will only be available for the"
            " selected company."
        ),
    )

    url_invitation_redirect = fields.Char(
        help="Will be the url send to user by email."
    )

    company_website_id = fields.Many2one(
        comodel_name="website",
        string="website",
        help="Will be use for email invitation.",
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
        # Automatic accept, create member
        if (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("ore.ore_auto_accept_adhesion")
        ):
            default_ore_society = (
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("ore.ore_default_societe")
            )
            ore_default_free_time = (
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("ore.ore_default_free_time", 0)
            )
            if not default_ore_society:
                raise Exception(
                    "Need to define ORE society, please contact the"
                    " administrator."
                )
            society_id = self.env["ore.membre"].browse(
                int(default_ore_society)
            )
            # TODO move this into ore, do refactoring (merge partner and member), add configuration
            lst_data = []
            for rec in vals:
                if rec.only_invitation:
                    continue
                data = {
                    "profil_approuver": True,
                    "name": rec.nom_complet,
                    # "parent_id": self.env.ref("base.main_partner").id,
                    # "reseau_ore_id": society_id.id,
                    "user_id": rec.user_id.id,
                    "partner_id": rec.user_id.partner_id.id,
                    "region": society_id.region.id,
                    "ville": society_id.ville.id,
                    "ore_client_key": uuid.uuid4().hex,
                }
                if rec.clan_id:
                    data["clan_principal_id"] = rec.clan_id.id
                    data["clan_participe_ids"] = [(6, 0, rec.clan_id.id)]
                lst_data.append(data)
            if lst_data:
                membre_ids = self.env["ore.membre"].create(lst_data)
                # Force add initial time
                lst_data_echange = []
                for membre_id in membre_ids:
                    data = {
                        "date_echange": fields.Datetime.now(),
                        "nb_heure": float(ore_default_free_time),
                        "type_echange": "offre_ponctuel",
                        "transaction_valide": True,
                        "membre_acheteur": society_id.id,
                        "membre_vendeur": membre_id.id,
                    }
                    lst_data_echange.append(data)
                self.env["ore.echange.service"].create(lst_data_echange)
        return vals

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
                f"http://{rec.company_website_id.domain}/chercher_clan"
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
