from odoo import models, fields, api


class HRDashboardWizard(models.TransientModel):
    _name = 'hr.dashboard.wizard'
    _description = 'HR Dashboard'

    name = fields.Char(default="Dashboard")

    tong_nhan_vien = fields.Integer(compute="_compute_data")
    tong_luong = fields.Float(compute="_compute_data")
    tong_thuong = fields.Float(compute="_compute_data")
    tong_phat = fields.Float(compute="_compute_data")

    def _compute_data(self):
        phieu = self.env['hr.phieu.luong'].search([])
        nhanvien = self.env['nhan_vien'].search([])

        self.tong_nhan_vien = len(nhanvien)
        self.tong_luong = sum(p.thuc_linh for p in phieu)
        self.tong_thuong = sum(p.tong_thuong for p in phieu)
        self.tong_phat = sum(p.tong_phat for p in phieu)
