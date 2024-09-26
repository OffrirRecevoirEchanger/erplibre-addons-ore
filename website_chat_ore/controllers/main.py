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

        lst_membre_message = []
        membre_message_ids = http.request.env["ore.chat.group"].search(
            [("membre_ids", "in", [membre_id.id])]
        )
        for membre_message_id in membre_message_ids:
            if membre_message_id.clan_id or membre_message_id.group_clan_id:
                continue
            dct_membre_message = membre_message_id.first_to_json(membre_id.id)
            notif_membre_id = http.request.env["ore.notification.chat"].search(
                [
                    ("group_id", "=", membre_message_id.id),
                    ("membre_notify_id", "=", membre_id.id),
                ]
            )
            # Add notification
            if not notif_membre_id:
                # Create new notification
                value_notif = {
                    "group_id": membre_message_id.id,
                    "membre_notify_id": membre_id.id,
                    "is_read": False,
                }
                notif_membre_id = http.request.env[
                    "ore.notification.chat"
                ].create(value_notif)
            dct_membre_message["is_read"] = notif_membre_id.is_read
            dct_membre_message["notif_id"] = notif_membre_id.id
            lst_membre_message.append(dct_membre_message)

        lst_clan_message = []
        clan_message_ids = http.request.env["ore.chat.group"].search(
            [("clan_id", "in", membre_id.clan_participe_ids.ids)]
        )
        for clan_message_id in clan_message_ids:
            if not clan_message_id.clan_id:
                continue
            dct_clan_message = clan_message_id.first_to_json()
            notif_clan_id = http.request.env["ore.notification.chat"].search(
                [
                    ("group_id", "=", clan_message_id.id),
                    ("membre_notify_id", "=", membre_id.id),
                ]
            )
            # Add notification
            if not notif_clan_id:
                # Create new notification
                value_notif = {
                    "group_id": clan_message_id.id,
                    "membre_notify_id": membre_id.id,
                    "is_read": False,
                }
                notif_clan_id = http.request.env[
                    "ore.notification.chat"
                ].create(value_notif)
            dct_clan_message["is_read"] = notif_clan_id.is_read
            dct_clan_message["notif_id"] = notif_clan_id.id
            lst_clan_message.append(dct_clan_message)

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

        # Remove notification for this user
        notif_ids = http.request.env["ore.notification.chat"].search(
            [
                ("group_id", "=", group_id),
                ("is_read", "=", False),
                ("membre_notify_id", "=", me_membre_id.id),
            ]
        )
        for notif_id in notif_ids:
            notif_id.write({"is_read": True})

        # Update notification for other users
        group_obj_id = http.request.env["ore.chat.group"].browse(group_id)
        if group_obj_id:
            lst_membre_to_notify = [a for a in group_obj_id.membre_ids]
            if not lst_membre_to_notify and group_obj_id.clan_id:
                lst_membre_to_notify = [
                    a for a in group_obj_id.clan_id.membre_list_ids
                ]
            if me_membre_id in lst_membre_to_notify:
                lst_membre_to_notify.remove(me_membre_id)
            for membre_obj_id in lst_membre_to_notify:
                notif_ids = http.request.env["ore.notification.chat"].search(
                    [
                        ("group_id", "=", group_id),
                        ("is_read", "=", True),
                        ("membre_notify_id", "=", membre_obj_id.id),
                    ]
                )
                for notif_id in notif_ids:
                    notif_id.write({"is_read": False})

        status = {"msg_id": message_id.id, "msg": msg}
        return status

    @http.route(
        "/ore/set_message_read",
        type="json",
        auth="user",
        website=True,
        csrf=True,
    )
    def ore_set_message_read(self, **kw):
        # Set read or unread a message
        # TODO better to force goal value and not only switch
        notif_id_i = kw.get("notif_id")
        msg_id = http.request.env["ore.notification.chat"].browse(notif_id_i)
        if msg_id:
            msg_id.is_read = not msg_id.is_read
            return {"is_read": msg_id.is_read}
        return {"error": f"Cannot find notif id '{notif_id_i}'"}

    @http.route(
        "/ore/notification_toute_lu",
        type="json",
        auth="user",
        website=True,
        csrf=True,
    )
    def ore_notification_toute_lu(self, **kw):
        # Set read or unread a message
        membre_id_i = kw.get("membre_id_i")
        type_notif = kw.get("type")
        if type_notif == "membre":
            msg_ids = http.request.env["ore.notification.chat"].search(
                [
                    ("membre_notify_id", "=", membre_id_i),
                    ("group_id.clan_id", "=", False),
                ]
            )
        elif type_notif == "group":
            msg_ids = http.request.env["ore.notification.chat"].search(
                [
                    ("membre_notify_id", "=", membre_id_i),
                    ("group_id.clan_id", "!=", False),
                ]
            )
        elif type_notif == "notif":
            # TODO Need to be into module website_ore or ore, not website_chat_ore
            msg_ids = http.request.env[
                "ore.echange.service.notification"
            ].search([("membre_id", "=", membre_id_i)])
        else:
            return {
                "error": (
                    "Cannot find notification type to set as read. Receive"
                    f" notif type {type_notif}"
                )
            }
        for msg_id in msg_ids:
            msg_id.is_read = True
        return {"status": True}
