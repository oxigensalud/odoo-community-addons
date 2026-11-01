# Copyright NuoBiT Solutions - Eric Antones <eantones@nuobit.com>
# Copyright 2025 NuoBiT Solutions - Deniz Gallo <dgallo@nuobit.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PriceListTags(models.Model):
    _name = "pricelist.tags"
    _description = "Pricelist tags"

    name = fields.Char()
    active = fields.Boolean(default=True)
    parent_id = fields.Many2one(
        comodel_name="pricelist.tags",
        ondelete="restrict",
    )
    display_name = fields.Char(
        compute="_compute_display_name",
        recursive=True,
        store=True,
    )

    _sql_constraints = [("name", "unique (name)", "The name must be unique !")]

    @api.constrains("parent_id")
    def _check_hierarchy(self):
        for record in self:
            if record._has_cycle():
                raise ValidationError(_("Error! You cannot add recursive categories."))

    @api.depends("name", "parent_id.display_name")
    def _compute_display_name(self):
        for record in self:
            names = []
            current = record
            while current:
                if current.name:
                    names.append(current.name)
                current = current.parent_id
            record.display_name = " / ".join(reversed(names)) if names else ""

    @api.model
    def name_search(self, name, args=None, operator="ilike", limit=100):
        args = args or []
        if name:
            name = name.split(" / ")[-1]
            args = [("name", operator, name)] + args
        recs = self.search(args, limit=limit)
        return [(rec.id, rec.display_name) for rec in recs]
