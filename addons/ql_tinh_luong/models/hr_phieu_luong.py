from odoo import models, fields, api


class HRPhieuLuong(models.Model):
    _name = 'hr.phieu.luong'
    _description = 'Phiếu lương'

    nhan_vien_id = fields.Many2one('nhan_vien', string='Nhân viên', required=True)

    thang = fields.Integer(string='Tháng', required=True)
    nam = fields.Integer(string='Năm', required=True)

    luong_co_ban = fields.Float(string='Lương cơ bản', default=5000000)

    tong_cong = fields.Float(compute='_compute_luong', store=True)
    tong_thuong = fields.Float(compute='_compute_luong', store=True)
    tong_phat = fields.Float(compute='_compute_luong', store=True)
    thuc_linh = fields.Float(compute='_compute_luong', store=True)

    @api.depends('nhan_vien_id', 'thang', 'nam', 'luong_co_ban')
    def _compute_luong(self):
        for rec in self:

            if not rec.nhan_vien_id:
                rec.tong_cong = 0
                rec.tong_thuong = 0
                rec.tong_phat = 0
                rec.thuc_linh = 0
                continue

            cham_cong = self.env['hr.cham.cong'].search([
                ('nhan_vien_id', '=', rec.nhan_vien_id.id),
                ('thang', '=', rec.thang),
                ('nam', '=', rec.nam),
                ('trang_thai', '=', 'di_lam')
            ])

            so_ngay_cong = len(cham_cong)

            quyet_dinh = self.env['hr.khen.thuong.ky.luat'].search([
                ('nhan_vien_id', '=', rec.nhan_vien_id.id),
                ('thang', '=', rec.thang),
                ('nam', '=', rec.nam),
            ])

            tong_thuong = sum(x.so_tien for x in quyet_dinh if x.loai_quyet_dinh == 'thuong')
            tong_phat = sum(x.so_tien for x in quyet_dinh if x.loai_quyet_dinh == 'phat')

            luong_ngay = rec.luong_co_ban / 26

            rec.tong_cong = so_ngay_cong
            rec.tong_thuong = tong_thuong
            rec.tong_phat = tong_phat
            rec.thuc_linh = (so_ngay_cong * luong_ngay) + tong_thuong - tong_phat
