# Copyright 2023 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # TODO: Review rename maintenance_lot to create_equipment_at_reception or similar
    maintenance_lot = fields.Boolean(string="Create eq. at reception")
    maintenance_category_id = fields.Many2one("maintenance.equipment.category")
    maintenance_team_id = fields.Many2one("maintenance.team")
