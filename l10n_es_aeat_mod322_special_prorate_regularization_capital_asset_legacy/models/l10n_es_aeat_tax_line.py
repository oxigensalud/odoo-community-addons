# Copyright Dixmit
# Copyright 2026 NuoBiT Solutions SL - Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.osv import expression
from odoo.osv.query import Query


class L10nEsAeatTaxLine(models.Model):
    _inherit = "l10n.es.aeat.tax.line"

    asset_ids = fields.Many2many(
        string="Assets",
        comodel_name="account.asset",
    )
    mod322_id = fields.Many2one(
        string="Model 322",
        comodel_name="l10n.es.aeat.mod322.report",
        compute="_compute_mod322_id",
        search="_search_mod322_id",
    )
    mod322_period_type = fields.Selection(related="mod322_id.period_type")

    def _compute_mod322_id(self):
        for rec in self:
            if rec.model == "l10n.es.aeat.mod322.report":
                rec.mod322_id = self.env[rec.model].browse(rec.res_id)
            else:
                rec.mod322_id = False

    @api.model
    def _search_mod322_id(self, operator, value):
        def is_record_id(v):
            # True is an int too
            return isinstance(v, int) and not isinstance(v, bool) and v > 0

        if operator not in ("=", "!=", "in", "not in"):
            raise NotImplementedError(
                _("Unsupported operator %s for Model 322 search") % operator
            )
        # res_id 0 means no 322, as in the compute
        mod322_domain = [
            "&",
            ("model", "=", "l10n.es.aeat.mod322.report"),
            ("res_id", "!=", 0),
        ]
        if operator == "in" and isinstance(value, Query):
            # Subquery from a mod322_period_type search
            domain = expression.AND([mod322_domain, [("res_id", "in", value)]])
        else:
            # None alone means no 322, as in Odoo; in a list it is refused
            values = (
                [value if value is not None else False]
                if operator in ("=", "!=")
                else value
            )
            if not isinstance(values, (list, tuple)) or not all(
                v is False or is_record_id(v) for v in values
            ):
                raise NotImplementedError(
                    _("Unsupported value %s for Model 322 search") % repr(value)
                )
            report_ids = [v for v in values if v is not False]
            domain = expression.AND([mod322_domain, [("res_id", "in", report_ids)]])
            if len(report_ids) < len(values):
                # False also matches the lines without a 322
                domain = expression.OR(
                    [domain, [expression.NOT_OPERATOR] + mod322_domain]
                )
        # model and res_id are required, so the negation is exact
        return (
            [expression.NOT_OPERATOR] + domain
            if operator in ("!=", "not in")
            else domain
        )

    def get_calculated_assets(self):
        action_dict = (
            self.env.ref("account_asset_management.account_asset_action")
            .sudo()
            .read()[0]
        )
        action_dict["domain"] = [("id", "in", self.asset_ids.ids)]
        return action_dict
