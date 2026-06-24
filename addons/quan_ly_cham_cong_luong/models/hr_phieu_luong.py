from odoo import models, fields, api


class HrPhieuLuong(models.Model):
    _name = 'hr_phieu_luong'
    _description = 'Phiếu lương tháng'
    _order = 'nam desc, thang desc, id desc'

    ten_phieu_luong = fields.Char(
        string='Tên phiếu lương',
        required=True,
        default='Phiếu lương tháng'
    )

    nhan_vien_id = fields.Many2one(
        'nhan_vien',
        string='Nhân viên',
        required=True
    )

    ma_dinh_danh = fields.Char(
        string='Mã định danh',
        related='nhan_vien_id.ma_dinh_danh',
        store=True,
        readonly=True
    )

    thang = fields.Selection([
        ('1', 'Tháng 1'),
        ('2', 'Tháng 2'),
        ('3', 'Tháng 3'),
        ('4', 'Tháng 4'),
        ('5', 'Tháng 5'),
        ('6', 'Tháng 6'),
        ('7', 'Tháng 7'),
        ('8', 'Tháng 8'),
        ('9', 'Tháng 9'),
        ('10', 'Tháng 10'),
        ('11', 'Tháng 11'),
        ('12', 'Tháng 12'),
    ], string='Tháng', required=True, default=lambda self: str(fields.Date.today().month))

    nam = fields.Integer(
        string='Năm',
        required=True,
        default=lambda self: fields.Date.today().year
    )

    so_ngay_cong_tinh_luong = fields.Float(
        string='Số ngày công tính lương',
        default=0
    )

    luong_co_ban = fields.Float(
        string='Lương cơ bản',
        default=0
    )

    phu_cap = fields.Float(
        string='Phụ cấp',
        default=0
    )

    tong_khen_thuong = fields.Float(
        string='Tổng khen thưởng',
        default=0
    )

    tong_ky_luat = fields.Float(
        string='Tổng kỷ luật',
        default=0
    )

    tien_bao_hiem = fields.Float(
        string='Tiền bảo hiểm',
        default=0
    )

    thuc_linh = fields.Float(
        string='Thực lĩnh',
        compute='_compute_thuc_linh',
        store=True
    )

    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('xac_nhan', 'Đã xác nhận'),
        ('thanh_toan', 'Đã thanh toán'),
    ], string='Trạng thái', default='nhap')

    ghi_chu = fields.Text(string='Ghi chú')

    @api.depends(
        'luong_co_ban',
        'phu_cap',
        'tong_khen_thuong',
        'tong_ky_luat',
        'tien_bao_hiem',
        'so_ngay_cong_tinh_luong'
    )
    def _compute_thuc_linh(self):
        for rec in self:
            luong_theo_ngay_cong = 0

            if rec.luong_co_ban:
                luong_theo_ngay_cong = (rec.luong_co_ban / 26.0) * rec.so_ngay_cong_tinh_luong

            rec.thuc_linh = (
                luong_theo_ngay_cong
                + rec.phu_cap
                + rec.tong_khen_thuong
                - rec.tong_ky_luat
                - rec.tien_bao_hiem
            )

    def action_xac_nhan(self):
        for rec in self:
            rec.trang_thai = 'xac_nhan'

    def action_thanh_toan(self):
        for rec in self:
            rec.trang_thai = 'thanh_toan'

    def action_dua_ve_nhap(self):
        for rec in self:
            rec.trang_thai = 'nhap'
