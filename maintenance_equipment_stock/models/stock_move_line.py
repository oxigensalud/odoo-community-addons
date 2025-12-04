# Copyright 2023 Dixmit
# Copyright NuoBiT - Frank Cespedes <fcespedes@nuobit.com>
# Copyright 2025 NuoBiT Solutions - Deniz Gallo <dgallo@nuobit.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import ValidationError


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _get_maintenance_equipment_by_ml_data(self, maintenance_equipment):
        values = {"stock_location_id": self.location_dest_id.id}
        if self.move_id.picking_type_id.code == "incoming":
            move_lines = self.env["stock.move.line"].search(
                [("lot_id", "=", self.lot_id.id), ("id", "!=", self.id)]
            )
            if maintenance_equipment.picking_id.picking_type_id.code == "incoming":
                raise ValidationError(
                    _(
                        "Maintenance Equipment already exists for this lot. It is "
                        "likely that a return of the lot was made, which is why the "
                        "maintenance equipment exists. Please fix this or contact the "
                        "administrator for further support."
                    )
                )
            elif move_lines:
                raise ValidationError(
                    _(
                        "Maintenance Equipment already exists for this lot. Movements "
                        "have been made with this lot, which is why the maintenance "
                        "equipment exists. Please fix this or contact the administrator"
                        " for further support."
                    )
                )
            else:
                values.update(
                    {
                        "picking_id": self.move_id.picking_id.id,
                        "purchase_id": self.move_id.picking_id.purchase_id.id,
                    }
                )
        return values

    def _update_maintenance_equipment_by_ml(self, maintenance_equipment):
        maintenance_equipment.write(
            self._get_maintenance_equipment_by_ml_data(maintenance_equipment)
        )

    def _action_done(self):
        result = super()._action_done()
        for ml in self.filtered(lambda m: m.exists()):
            if (
                ml.product_id.is_storable
                and ml.product_id.tracking == "serial"
                and ml.move_id.picking_type_id.code in ["incoming", "internal"]
            ):
                maintenance_equipment = self.env["maintenance.equipment"].search(
                    [("lot_id", "=", ml.lot_id.id)]
                )
                if maintenance_equipment:
                    ml._update_maintenance_equipment_by_ml(maintenance_equipment)
                elif (
                    ml.product_id.maintenance_lot
                    and ml.move_id.picking_type_id.code == "incoming"
                ):
                    ml._create_maintenance_equipment()
        return result

    def _create_maintenance_equipment(self):
        return self.env["maintenance.equipment"].create(
            self._create_maintenance_equipment_vals()
        )

    def _create_maintenance_equipment_vals(self):
        return {
            "lot_id": self.lot_id.id,
            "picking_id": self.move_id.picking_type_id.code == "incoming"
            and self.move_id.picking_id.id,
            "stock_move_line_id": self.id,
            "name": self.product_id.display_name,
            # "company_id": self.company_id.id,
            "company_id": False,
            "partner_id": self.move_id.picking_id.partner_id.id,
            "category_id": self.product_id.maintenance_category_id.id,
            "maintenance_team_id": self.product_id.maintenance_team_id.id,
            "purchase_id": self.move_id.picking_id.purchase_id.id,
            "stock_location_id": self.location_dest_id.id,
        }
