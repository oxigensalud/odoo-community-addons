# Copyright NuoBiT Solutions - Eric Antones <eantones@nuobit.com>
# Copyright 2025 NuoBiT Solutions - Deniz Gallo <dgallo@nuobit.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
{
    "name": "Price List Massive Update",
    "summary": "Update pricelists according to pricelist tags",
    "version": "18.0.1.0.0",
    "category": "Sale",
    "license": "AGPL-3",
    "author": "Vraja Technologies, Oxigen Salud SA",
    "website": "https://github.com/oxigensalud/odoo-community-addons",
    "depends": ["base", "sale"],
    "data": [
        "security/ir.model.access.csv",
        "views/pricelist_tags.xml",
        "views/product_pricelist.xml",
        "views/pricelist_update.xml",
    ],
}
