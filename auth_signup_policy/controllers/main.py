# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import _, http
from odoo.addons.auth_signup.controllers.main import AuthSignupHome as Home
from odoo.http import request


class AuthSignupHome(Home):
    @http.route()
    def web_auth_signup(self, *args, **kw):
        status = super().web_auth_signup(*args, **kw)

        enable_sign_up_connection_policy = bool(
            request.env["ir.config_parameter"]
            .sudo()
            .get_param("enable_sign_up_connection_policy")
        )
        enable_sign_up_privacy_policy = bool(
            request.env["ir.config_parameter"]
            .sudo()
            .get_param("enable_sign_up_privacy_policy")
        )
        enable_sign_up_terms_of_service = bool(
            request.env["ir.config_parameter"]
            .sudo()
            .get_param("enable_sign_up_terms_of_service")
        )

        sign_up_connection_policy_body_translate = (
            request.env["ir.translation"]
            .sudo()
            .search(
                [
                    (
                        "name",
                        "=",
                        "res.config.settings,sign_up_connection_policy_body",
                    ),
                    ("lang", "=", request.context.get("lang")),
                ],
                limit=1,
            )
            .exists()
        )
        if sign_up_connection_policy_body_translate:
            sign_up_connection_policy_body = (
                sign_up_connection_policy_body_translate.value
            )
        else:
            sign_up_connection_policy_body = (
                request.env["ir.config_parameter"]
                .sudo()
                .get_param("sign_up_connection_policy_body")
            )

        status.qcontext.update(
            {
                "enable_sign_up_connection_policy": enable_sign_up_connection_policy,
                "enable_sign_up_privacy_policy": enable_sign_up_privacy_policy,
                "enable_sign_up_terms_of_service": enable_sign_up_terms_of_service,
                "sign_up_connection_policy_body": sign_up_connection_policy_body,
                "enable_sign_up_global_policy": enable_sign_up_connection_policy
                + enable_sign_up_privacy_policy
                + enable_sign_up_terms_of_service,
            }
        )
        return status
