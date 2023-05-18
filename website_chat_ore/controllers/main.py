import logging

from odoo import _, http
from odoo.http import request

_logger = logging.getLogger(__name__)


class OREController(http.Controller):
    @staticmethod
    def get_membre_id():
        partner_id = http.request.env.user.partner_id
        # TODO wrong algorithm, but use instead 'auth="user",'
        if not partner_id or http.request.auth_method == "public":
            return {"error": _("User not connected")}

        membre_id = request.env["res.partner"].browse(partner_id.id)

        if not membre_id:
            return {
                "error": _(
                    "Your account is not associate to an ore"
                    " configuration. Please contact your administrator."
                )
            }
        return membre_id

    @http.route(
        [
            "/ore/get_personal_chat_information",
        ],
        type="json",
        auth="user",
        website=True,
    )
    def get_personal_chat_information(self, **kw):
        membre_id = self.get_membre_id()
        if type(membre_id) is dict:
            # This is an error
            return membre_id

        lst_membre_message = [
            a.first_to_json(membre_id.id)
            for a in http.request.env["ore.chat.group"].search(
                [("membre_ids", "in", [membre_id.id])]
            )
        ]

        return {
            "lst_membre_message": lst_membre_message,
        }

    @http.route(
        "/ore/submit/chat_msg",
        type="json",
        auth="user",
        website=True,
        csrf=True,
    )
    def ore_chat_msg_submit(self, **kw):
        msg = kw.get("msg")
        group_id = kw.get("group_id")
        membre_id = kw.get("membre_id")
        me_membre_id = http.request.env.user.partner_id
        if not group_id:
            group_value = {
                "membre_ids": [(6, 0, [membre_id, me_membre_id.id])]
            }
            group_id_id = http.request.env["ore.chat.group"].create(
                group_value
            )
            group_id = group_id_id.id
        value = {
            "name": msg,
            "membre_writer_id": me_membre_id.id,
            "msg_group_id": group_id,
        }
        message_id = http.request.env["ore.chat.message"].create(value)

        status = {"msg_id": message_id}
        return status
