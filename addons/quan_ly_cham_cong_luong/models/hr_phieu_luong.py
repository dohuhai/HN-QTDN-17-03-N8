from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class HRPhieuLuong(models.Model):
    _name = 'hr_phieu_luong'
    _description = 'Phiếu lương tháng'
    _rec_name = 'ten_phieu_luong'
    _order = 'nam desc, thang desc'

    ten_phieu_luong = fields.Char(
        string='Tên phiếu lương',
        compute='_compute_ten_phieu_luong',
        store=True
    )

    nhan_vien_id = fields.Many2one(
        'nhan_vien',
        string='Nhân viên',
        required=True
    )

    ma_dinh_danh = fields.Char(
        string='Mã định danh',
        related='nhan_vien_id.ma_dinh_danh',
        store=True
    )

    thang = fields.Integer(
        string='Tháng',
        required=True,
        default=lambda self: date.today().month
    )

    nam = fields.Integer(
        string='Năm',
        required=True,
        default=lambda self: date.today().year
    )

    so_ngay_di_lam = fields.Float(
        string='Số ngày đi làm đủ',
        compute='_compute_du_lieu_luong',
        store=True
    )

    so_ngay_nua_ngay = fields.Float(
        string='Số ngày làm nửa ngày',
        compute='_compute_du_lieu_luong',
        store=True
    )

    so_ngay_nghi_co_phep = fields.Float(
        string='Số ngày nghỉ có phép',
        compute='_compute_du_lieu_luong',
        store=True
    )

    so_ngay_nghi_khong_phep = fields.Float(
        string='Số ngày nghỉ không phép',
        compute='_compute_du_lieu_luong',
        store=True
    )

    so_ngay_cong_tinh_luong = fields.Float(
        string='Số ngày công tính lương',
        compute='_compute_du_lieu_luong',
        store=True
    )

    tong_gio_tang_ca = fields.Float(
        string='Tổng giờ tăng ca',
        compute='_compute_du_lieu_luong',
        store=True
    )

    luong_co_ban = fields.Float(
        string='Lương cơ bản',
        compute='_compute_du_lieu_luong',
        store=True
    )

    phu_cap = fields.Float(
        string='Tổng phụ cấp',
        compute='_compute_du_lieu_luong',
        store=True
    )

    tong_khen_thuong = fields.Float(
        string='Tổng khen thưởng',
        compute='_compute_du_lieu_luong',
        store=True
    )

    tong_ky_luat = fields.Float(
        string='Tổng kỷ luật',
        compute='_compute_du_lieu_luong',
        store=True
    )

    ty_le_bao_hiem = fields.Float(
        string='Tỷ lệ bảo hiểm nhân viên (%)',
        default=10.5
    )

    tien_bao_hiem = fields.Float(
        string='Tiền bảo hiểm',
        compute='_compute_du_lieu_luong',
        store=True
    )

    tong_thu_nhap = fields.Float(
        string='Tổng thu nhập trước bảo hiểm',
        compute='_compute_du_lieu_luong',
        store=True
    )

    thuc_linh = fields.Float(
        string='Thực lĩnh',
        compute='_compute_du_lieu_luong',
        store=True
    )

    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('xac_nhan', 'Đã xác nhận'),
        ('huy', 'Đã hủy')
    ], string='Trạng thái', default='nhap')

    ghi_chu = fields.Text(
        string='Ghi chú'
    )

    @api.constrains('thang', 'nam')
    def _check_thang_nam(self):
        for record in self:
            if record.thang < 1 or record.thang > 12:
                raise ValidationError('Tháng phải nằm trong khoảng từ 1 đến 12.')
            if record.nam < 2000:
                raise ValidationError('Năm không hợp lệ.')

    @api.depends('nhan_vien_id', 'thang', 'nam')
    def _compute_ten_phieu_luong(self):
        for record in self:
            if record.nhan_vien_id:
                record.ten_phieu_luong = 'Phiếu lương %s - Tháng %s/%s' % (
                    record.nhan_vien_id.ho_va_ten,
                    record.thang,
                    record.nam
                )
            else:
                record.ten_phieu_luong = 'Phiếu lương tháng %s/%s' % (
                    record.thang,
                    record.nam
                )

    @api.depends('nhan_vien_id', 'thang', 'nam', 'ty_le_bao_hiem')
    def _compute_du_lieu_luong(self):
        for record in self:
            record.so_ngay_di_lam = 0
            record.so_ngay_nua_ngay = 0
            record.so_ngay_nghi_co_phep = 0
            record.so_ngay_nghi_khong_phep = 0
            record.so_ngay_cong_tinh_luong = 0
            record.tong_gio_tang_ca = 0
            record.luong_co_ban = 0
            record.phu_cap = 0
            record.tong_khen_thuong = 0
            record.tong_ky_luat = 0
            record.tien_bao_hiem = 0
            record.tong_thu_nhap = 0
            record.thuc_linh = 0

            if not record.nhan_vien_id or not record.thang or not record.nam:
                continue

            ngay_bat_dau = date(record.nam, record.thang, 1)

            if record.thang == 12:
                ngay_ket_thuc = date(record.nam + 1, 1, 1)
            else:
                ngay_ket_thuc = date(record.nam, record.thang + 1, 1)

            cham_cong_records = self.env['hr_cham_cong'].search([
                ('nhan_vien_id', '=', record.nhan_vien_id.id),
                ('ngay_cham_cong', '>=', ngay_bat_dau),
                ('ngay_cham_cong', '<', ngay_ket_thuc),
            ])

            record.so_ngay_di_lam = len(
                cham_cong_records.filtered(lambda r: r.trang_thai == 'di_lam')
            )

            record.so_ngay_nua_ngay = len(
                cham_cong_records.filtered(lambda r: r.trang_thai == 'nua_ngay')
            )

            record.so_ngay_nghi_co_phep = len(
                cham_cong_records.filtered(lambda r: r.trang_thai == 'nghi_co_phep')
            )

            record.so_ngay_nghi_khong_phep = len(
                cham_cong_records.filtered(lambda r: r.trang_thai == 'nghi_khong_phep')
            )

            record.so_ngay_cong_tinh_luong = (
                record.so_ngay_di_lam + record.so_ngay_nua_ngay * 0.5
            )

            record.tong_gio_tang_ca = sum(cham_cong_records.mapped('so_gio_tang_ca'))

            cau_hinh_luong = self.env['hr_luong_co_ban'].search([
                ('nhan_vien_id', '=', record.nhan_vien_id.id)
            ], limit=1)

            if cau_hinh_luong:
                record.luong_co_ban = cau_hinh_luong.luong_co_ban
                record.phu_cap = (
                    cau_hinh_luong.phu_cap_an_trua
                    + cau_hinh_luong.phu_cap_trach_nhiem
                    + cau_hinh_luong.phu_cap_khac
                )

            bien_dong_records = self.env['hr_khen_thuong_ky_luat'].search([
                ('nhan_vien_id', '=', record.nhan_vien_id.id),
                ('ngay_ap_dung', '>=', ngay_bat_dau),
                ('ngay_ap_dung', '<', ngay_ket_thuc),
            ])

            record.tong_khen_thuong = sum(
                bien_dong_records
                .filtered(lambda r: r.loai_quyet_dinh == 'khen_thuong')
                .mapped('so_tien')
            )

            record.tong_ky_luat = sum(
                bien_dong_records
                .filtered(lambda r: r.loai_quyet_dinh == 'ky_luat')
                .mapped('so_tien')
            )

            tien_luong_theo_cong = (
                record.luong_co_ban / 26
            ) * record.so_ngay_cong_tinh_luong

            record.tong_thu_nhap = (
                tien_luong_theo_cong
                + record.phu_cap
                + record.tong_khen_thuong
                - record.tong_ky_luat
            )

            record.tien_bao_hiem = record.luong_co_ban * record.ty_le_bao_hiem / 100
            record.thuc_linh = record.tong_thu_nhap - record.tien_bao_hiem

    def action_xac_nhan(self):
        for record in self:
            record.trang_thai = 'xac_nhan'

    def action_dat_ve_nhap(self):
        for record in self:
            record.trang_thai = 'nhap'

    def action_huy(self):
        for record in self:
            record.trang_thai = 'huy'
