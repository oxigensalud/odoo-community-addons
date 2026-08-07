# Copyright 2026 NuoBiT Solutions SL - Deniz Gallo <dgallo@nuobit.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from psycopg2 import IntegrityError

from odoo import api, fields, models


class SpmsErrorType(models.Model):
    _name = "spms.error.type"
    _description = "SPMS Error Type"
    _order = "code"
    _rec_name = "code"

    code = fields.Char(
        required=True,
        index=True,
    )
    description = fields.Char(
        string="Official Message (PT)",
        help="Error message exactly as the CCF check documents report it.",
    )
    note = fields.Char(
        help="Internal note about what this error means for the " "invoicing workflow.",
    )
    usual_level = fields.Selection(
        selection=[
            ("invoice", "Invoice"),
            ("lote", "Lot"),
            ("prestacao", "Claim"),
            ("linha", "Line"),
            ("prescricao", "Prescription Data"),
        ],
        help="Informative: nesting point of the check document where this "
        "error is usually anchored.",
    )
    is_noise = fields.Boolean(
        string="Noise",
        help="Systematic noise: reported on almost every line of the "
        "affected invoices (e.g. C012), so lists and analyses may want "
        "to filter it out.",
    )
    to_classify = fields.Boolean(
        help="Set on codes auto-created by the check processing: the code "
        "was unknown and is pending human classification.",
    )

    _sql_constraints = [
        (
            "code_uniq",
            "unique(code)",
            "An error type with this code already exists.",
        ),
    ]

    def name_get(self):
        result = []
        for record in self:
            name = record.code
            if record.description:
                name = "%s - %s" % (record.code, record.description)
            result.append((record.id, name))
        return result

    @api.model
    def _get_or_create(self, code, message=None):
        """Return the error type for ``code``, creating it if unknown."""
        code = (code or "").strip()
        if not code:
            return self.browse()
        error_type = self.search([("code", "=", code)], limit=1)
        if not error_type:
            try:
                with self.env.cr.savepoint():
                    return self.create(
                        {
                            "code": code,
                            "description": message,
                            "to_classify": True,
                        }
                    )
            except IntegrityError:
                error_type = self.search([("code", "=", code)], limit=1)
        if message and not error_type.description:
            error_type.description = message
        return error_type
