# Copyright 2023 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class TestContactUser(SavepointCase):
    def test_partner_no_user(self):
        partner = self.env["res.partner"].create({"name": "My demo partner"})
        self.assertEqual(partner.user_count, 0)
        action = partner.show_user()
        self.assertEqual(action["res_model"], "res.users")
        self.assertFalse(action["res_id"])

    def test_partner_user(self):
        partner = self.env.user.partner_id.with_context(active_test=False)
        self.assertEqual(partner.user_count, 1)
        action = partner.show_user()
        self.assertEqual(action["res_model"], "res.users")
        self.assertEqual(action["res_id"], self.env.user.id)
