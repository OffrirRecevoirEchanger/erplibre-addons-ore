# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
from odoo import api, fields, models
from odoo.tools.translate import html_translate


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    enable_sign_up_connection_policy = fields.Boolean(
        "Show Connection Policy",
        help=(
            "On sign up, show connection policy, check content with"
            " sign_up_connection_policy_body"
        ),
    )
    enable_sign_up_privacy_policy = fields.Boolean(
        "Show Privacy Policy", help="On sign up, show privacy policy"
    )
    enable_sign_up_terms_of_service = fields.Boolean(
        "Show Terms of Service", help="On sign up, show terms of service"
    )
    sign_up_connection_policy_body = fields.Html(
        "Connection policy",
        help="On sign up, show terms of service",
        translate=html_translate,
    )

    @api.model
    def get_values(self):
        status = super(ResConfigSettings, self).get_values()

        IrConfigParameter = self.env["ir.config_parameter"].sudo()
        enable_sign_up_connection_policy = IrConfigParameter.get_param(
            "enable_sign_up_connection_policy", default=False
        )
        enable_sign_up_privacy_policy = IrConfigParameter.get_param(
            "enable_sign_up_privacy_policy", default=False
        )
        enable_sign_up_terms_of_service = IrConfigParameter.get_param(
            "enable_sign_up_terms_of_service", default=False
        )
        sign_up_connection_policy_body = IrConfigParameter.get_param(
            "sign_up_connection_policy_body", default=""
        )

        status.update(
            enable_sign_up_connection_policy=enable_sign_up_connection_policy,
            enable_sign_up_privacy_policy=enable_sign_up_privacy_policy,
            enable_sign_up_terms_of_service=enable_sign_up_terms_of_service,
            sign_up_connection_policy_body=sign_up_connection_policy_body,
        )
        return status

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env["ir.config_parameter"].set_param(
            "enable_sign_up_connection_policy",
            self.enable_sign_up_connection_policy,
        )
        self.env["ir.config_parameter"].set_param(
            "enable_sign_up_terms_of_service",
            self.enable_sign_up_terms_of_service,
        )
        self.env["ir.config_parameter"].set_param(
            "enable_sign_up_privacy_policy", self.enable_sign_up_privacy_policy
        )
        self.env["ir.config_parameter"].set_param(
            "sign_up_connection_policy_body",
            self.sign_up_connection_policy_body,
        )
