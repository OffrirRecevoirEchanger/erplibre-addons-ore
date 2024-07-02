import logging

from odoo import _, http
from odoo.http import request

_logger = logging.getLogger(__name__)


class OREController(http.Controller):
    @staticmethod
    def get_membre_id():
        membre_id = http.request.env.user.partner_id
        # TODO wrong algorithm, but use instead 'auth="user",'
        if not membre_id or http.request.auth_method == "public":
            return {"error": _("User not connected")}

        # # membre_id = partner_id.res_partner_ids
        # membre_id = request.env["ore.membre"].search(
        #     [("partner_id", "=", partner_id.id)], limit=1
        # )

        if not membre_id:
            return {
                "error": _(
                    "Your account is not "
                    " configuration. Please contact your administrator."
                )
            }
        ore_membre_id = (
            http.request.env["ore.membre"]
            .sudo()
            .search([("partner_id", "=", membre_id.id)], limit=1)
        )
        if not ore_membre_id:
            return {
                "error": _(
                    "Your account is not associate to an ore"
                    " configuration. Please contact your administrator."
                )
            }
        return ore_membre_id

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
            if not a.clan_id and not a.group_clan_id
        ]

        lst_clan_message = [
            a.first_to_json()
            for a in http.request.env["ore.chat.group"].search(
                [("clan_id", "in", membre_id.clan_participe_ids.ids)]
            )
            if a.clan_id
        ]

        return {
            "lst_membre_message": lst_membre_message,
            "lst_clan_message": lst_clan_message,
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
        clan_id = kw.get("clan_id")
        me_membre_id = self.get_membre_id()
        if not membre_id and not clan_id:
            return {
                "error": (
                    "Need argument membre_id or clan_id when send a message"
                    " from chat."
                )
            }
        if membre_id and clan_id:
            _logger.warning(
                "Ore chat is not suppose to support membre_id with clan_id,"
                " check method ore_chat_msg_submit"
            )
        if not group_id:
            # TODO need refactoring, only use group_id instead of clan_id
            if membre_id:
                group_value = {
                    "membre_ids": [(6, 0, [membre_id, me_membre_id.id])]
                }
                group_id_id = (
                    http.request.env["ore.chat.group"]
                    .sudo()
                    .create(group_value)
                )
                group_id = group_id_id.id
            elif clan_id:
                # check if exist before create a new one
                chat_group_id = http.request.env["ore.chat.group"].search(
                    [("clan_id", "=", clan_id)], limit=1
                )
                if chat_group_id:
                    group_id = chat_group_id.id
                else:
                    group_value = {"clan_id": clan_id}
                    group_id_id = (
                        http.request.env["ore.chat.group"]
                        .sudo()
                        .create(group_value)
                    )
                    group_id = group_id_id.id

        value = {
            "name": msg,
            "membre_writer_id": me_membre_id.id,
            "msg_group_id": group_id,
        }
        message_id = http.request.env["ore.chat.message"].create(value)

        status = {"msg_id": message_id.id, "msg": msg}
        return status
