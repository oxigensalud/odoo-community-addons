# Copyright 2026 NuoBiT Solutions SL - Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest.mock import patch

from odoo.osv import expression

from odoo.addons.l10n_es_aeat_mod322.tests.test_mod322 import TestL10nEsAeatMod322Base


class TestL10nEsAeatTaxLine(TestL10nEsAeatMod322Base):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.model322.button_calculate()
        cls.model322_4t.button_calculate()
        map_line = cls.model322.tax_line_ids[0].map_line_id
        # Another report's line on a 322's id (only the model name is used)
        cls.mod390_tax_line = cls.env["l10n.es.aeat.tax.line"].create(
            {
                "model": "l10n.es.aeat.mod390.report",
                "res_id": cls.model322.id,
                "map_line_id": map_line.id,
            }
        )
        # A 322 line pointing to no report
        cls.orphan_tax_line = cls.env["l10n.es.aeat.tax.line"].create(
            {
                "model": "l10n.es.aeat.mod322.report",
                "res_id": 0,
                "map_line_id": map_line.id,
            }
        )
        cls.tax_lines = cls.model322.tax_line_ids
        cls.tax_lines += cls.model322_4t.tax_line_ids
        cls.tax_lines += cls.mod390_tax_line
        cls.tax_lines += cls.orphan_tax_line

    def test_tax_line_search_mod322_in(self):
        tax_lines = self.env["l10n.es.aeat.tax.line"].search(
            [("id", "in", self.tax_lines.ids), ("mod322_id", "in", self.model322.ids)]
        )
        self.assertEqual(tax_lines, self.model322.tax_line_ids)

    def test_tax_line_search_mod322_in_both(self):
        tax_lines = self.env["l10n.es.aeat.tax.line"].search(
            [
                ("id", "in", self.tax_lines.ids),
                ("mod322_id", "in", [self.model322.id, self.model322_4t.id]),
            ]
        )
        self.assertEqual(
            tax_lines,
            self.model322.tax_line_ids + self.model322_4t.tax_line_ids,
        )

    def test_tax_line_search_mod322_equal(self):
        tax_lines = self.env["l10n.es.aeat.tax.line"].search(
            [("id", "in", self.tax_lines.ids), ("mod322_id", "=", self.model322_4t.id)]
        )
        self.assertEqual(tax_lines, self.model322_4t.tax_line_ids)

    def test_tax_line_search_mod322_not_equal(self):
        tax_lines = self.env["l10n.es.aeat.tax.line"].search(
            [("id", "in", self.tax_lines.ids), ("mod322_id", "!=", self.model322.id)]
        )
        self.assertEqual(
            tax_lines,
            self.model322_4t.tax_line_ids + self.mod390_tax_line + self.orphan_tax_line,
        )

    def test_tax_line_search_mod322_not_in(self):
        tax_lines = self.env["l10n.es.aeat.tax.line"].search(
            [
                ("id", "in", self.tax_lines.ids),
                ("mod322_id", "not in", self.model322.ids),
            ]
        )
        self.assertEqual(
            tax_lines,
            self.model322_4t.tax_line_ids + self.mod390_tax_line + self.orphan_tax_line,
        )

    def test_tax_line_search_mod322_not_in_both(self):
        tax_lines = self.env["l10n.es.aeat.tax.line"].search(
            [
                ("id", "in", self.tax_lines.ids),
                ("mod322_id", "not in", [self.model322.id, self.model322_4t.id]),
            ]
        )
        self.assertEqual(tax_lines, self.mod390_tax_line + self.orphan_tax_line)

    def test_tax_line_search_mod322_not_in_empty(self):
        tax_lines = self.env["l10n.es.aeat.tax.line"].search(
            [("id", "in", self.tax_lines.ids), ("mod322_id", "not in", [])]
        )
        self.assertEqual(tax_lines, self.tax_lines)

    def test_tax_line_search_mod322_false(self):
        tax_lines = self.env["l10n.es.aeat.tax.line"].search(
            [("id", "in", self.tax_lines.ids), ("mod322_id", "=", False)]
        )
        self.assertEqual(tax_lines, self.mod390_tax_line + self.orphan_tax_line)

    def test_tax_line_search_mod322_none(self):
        tax_lines = self.env["l10n.es.aeat.tax.line"].search(
            [("id", "in", self.tax_lines.ids), ("mod322_id", "=", None)]
        )
        self.assertEqual(tax_lines, self.mod390_tax_line + self.orphan_tax_line)

    def test_tax_line_search_mod322_not_false(self):
        tax_lines = self.env["l10n.es.aeat.tax.line"].search(
            [("id", "in", self.tax_lines.ids), ("mod322_id", "!=", False)]
        )
        self.assertEqual(
            tax_lines,
            self.model322.tax_line_ids + self.model322_4t.tax_line_ids,
        )

    def test_tax_line_search_mod322_in_or_false(self):
        tax_lines = self.env["l10n.es.aeat.tax.line"].search(
            [
                ("id", "in", self.tax_lines.ids),
                ("mod322_id", "in", [self.model322.id, False]),
            ]
        )
        self.assertEqual(
            tax_lines,
            self.model322.tax_line_ids + self.mod390_tax_line + self.orphan_tax_line,
        )

    def test_tax_line_search_mod322_not_in_nor_false(self):
        tax_lines = self.env["l10n.es.aeat.tax.line"].search(
            [
                ("id", "in", self.tax_lines.ids),
                ("mod322_id", "not in", [self.model322.id, False]),
            ]
        )
        self.assertEqual(tax_lines, self.model322_4t.tax_line_ids)

    def test_tax_line_search_mod322_period_type(self):
        tax_lines = self.env["l10n.es.aeat.tax.line"].search(
            [("id", "in", self.tax_lines.ids), ("mod322_period_type", "=", "12")]
        )
        self.assertEqual(tax_lines, self.model322_4t.tax_line_ids)

    def test_tax_line_search_mod322_unsupported_operator(self):
        with self.assertRaises(NotImplementedError):
            self.env["l10n.es.aeat.tax.line"].search(
                [("mod322_id", "ilike", self.model322.ids)]
            )

    def test_tax_line_search_mod322_name(self):
        with self.assertRaises(NotImplementedError):
            self.env["l10n.es.aeat.tax.line"].search(
                [("mod322_id", "=", self.model322.name)]
            )

    def test_tax_line_search_mod322_true(self):
        with self.assertRaises(NotImplementedError):
            self.env["l10n.es.aeat.tax.line"].search([("mod322_id", "=", True)])

    def test_tax_line_search_mod322_record(self):
        with self.assertRaises(NotImplementedError):
            self.env["l10n.es.aeat.tax.line"].search(
                [("mod322_id", "=", self.model322)]
            )

    def test_tax_line_search_mod322_zero(self):
        with self.assertRaises(NotImplementedError):
            self.env["l10n.es.aeat.tax.line"].search([("mod322_id", "in", [0])])

    def test_tax_line_search_mod322_none_in_list(self):
        with self.assertRaises(NotImplementedError):
            self.env["l10n.es.aeat.tax.line"].search(
                [("mod322_id", "in", [self.model322.id, None])]
            )

    def test_tax_line_search_mod322_not_in_subquery(self):
        reports_4t = self.env["l10n.es.aeat.mod322.report"]._search(
            [("period_type", "=", "12")]
        )
        with self.assertRaises(NotImplementedError):
            self.env["l10n.es.aeat.tax.line"].search(
                [("mod322_id", "not in", reports_4t)]
            )

    def test_tax_line_write_res_id(self):
        tax_line = self.model322.tax_line_ids[0]
        self.assertEqual(tax_line.mod322_id, self.model322)
        tax_line.write({"res_id": self.model322_4t.id})
        self.assertEqual(tax_line.mod322_id, self.model322_4t)

    def test_tax_line_write_model(self):
        tax_line = self.model322.tax_line_ids[0]
        self.assertEqual(tax_line.mod322_id, self.model322)
        tax_line.write({"model": "l10n.es.aeat.mod390.report"})
        self.assertFalse(tax_line.mod322_id)

    def test_mod322_write_period_type_refreshes_lines_without_error(self):
        tax_line = self.model322_4t.tax_line_ids[0]
        self.assertEqual(tax_line.mod322_period_type, "12")
        with patch.object(expression._logger, "error") as logger_error:
            self.model322_4t.write({"period_type": "11"})
        logger_error.assert_not_called()
        self.assertEqual(tax_line.mod322_period_type, "11")
