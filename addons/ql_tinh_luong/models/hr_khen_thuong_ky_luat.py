from odoo import models, fields


class HRKhenThuongKyLuat(models.Model):
    _name = 'hr.khen.thuong.ky.luat'
    _description = 'Khen thưởng và kỷ luật nhân viên'

    nhan_vien_id = fields.Many2one('nhan_vien', string='Nhân viên', required=True)

    loai_quyet_dinh = fields.Selection([
        ('thuong', 'Khen thưởng'),
        ('phat', 'Kỷ luật')
    ], string='Loại quyết định', required=True)

    so_tien = fields.Float(string='Số tiền', default=0.0)

    ngay_ap_dung = fields.Date(string='Ngày áp dụng', default=fields.Date.today)

    ghi_chu = fields.Text(string='Ghi chú')
