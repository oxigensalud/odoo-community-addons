# Copyright 2023 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):

    _inherit = "res.partner"

    user_count = fields.Integer(compute="_compute_user_count")

    @api.depends("user_ids")
    def _compute_user_count(self):
        for record in self:
            record.user_count = len(record.user_ids)

    def show_user(self):
        self.ensure_one()
        user = self.user_ids[:1]
        action = {
            "type": "ir.actions.act_window",
            "res_model": user._name,
            "view_type": "form",
            "view_mode": "form",
            "views": [(self.sudo().env.ref("base.view_users_form").id, "form")],
            "target": "current",
            "res_id": user.id,
            "context": dict(self._context),
        }
        if user:
            return action
        action["context"]["default_partner_id"] = self.id
        return action
