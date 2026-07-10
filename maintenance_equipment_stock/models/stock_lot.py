# Copyright 2023 Dixmit
# Copyright 2025 NuoBiT Solutions - Deniz Gallo <dgallo@nuobit.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockLot(models.Model):
    _inherit = "stock.lot"

    equipment_ids = fields.One2many(
        comodel_name="maintenance.equipment", inverse_name="lot_id"
    )

    def action_lot_open_equipment(self):
        self.ensure_one()
        return self.equipment_ids.get_formview_action()
