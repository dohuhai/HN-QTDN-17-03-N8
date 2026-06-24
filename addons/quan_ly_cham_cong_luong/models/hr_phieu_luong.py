from odoo import models, fields, api
from odoo.exceptions import UserError


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

    email_nhan_vien = fields.Char(
        string='Email nhân viên',
        related='nhan_vien_id.email',
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

    da_gui_email = fields.Boolean(
        string='Đã gửi email',
        default=False,
        readonly=True
    )

    ngay_gui_email = fields.Datetime(
        string='Ngày gửi email',
        readonly=True
    )

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

    def _format_money(self, amount):
        return '{:,.0f} VND'.format(amount or 0)

    def action_gui_email_phieu_luong(self):
        for rec in self:
            if rec.trang_thai not in ['xac_nhan', 'thanh_toan']:
                raise UserError('Chỉ được gửi email khi phiếu lương đã được xác nhận hoặc đã thanh toán.')

            if not rec.email_nhan_vien:
                raise UserError('Nhân viên chưa có email trong hồ sơ HRM. Vui lòng cập nhật email nhân viên trước khi gửi.')

            subject = 'Phiếu lương tháng %s/%s - Công ty TNHH Thương mại và Dịch vụ Minh Hải' % (
                rec.thang,
                rec.nam
            )

            body_html = """
                <div style="font-family: Arial, sans-serif; font-size: 14px;">
                    <p>Kính gửi <b>{nhan_vien}</b>,</p>

                    <p>
                        Công ty TNHH Thương mại và Dịch vụ Minh Hải gửi thông tin phiếu lương
                        tháng <b>{thang}/{nam}</b> của Anh/Chị như sau:
                    </p>

                    <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse;">
                        <tr>
                            <td><b>Mã định danh</b></td>
                            <td>{ma_dinh_danh}</td>
                        </tr>
                        <tr>
                            <td><b>Số ngày công tính lương</b></td>
                            <td>{so_ngay_cong}</td>
                        </tr>
                        <tr>
                            <td><b>Lương cơ bản</b></td>
                            <td>{luong_co_ban}</td>
                        </tr>
                        <tr>
                            <td><b>Phụ cấp</b></td>
                            <td>{phu_cap}</td>
                        </tr>
                        <tr>
                            <td><b>Tổng khen thưởng</b></td>
                            <td>{tong_khen_thuong}</td>
                        </tr>
                        <tr>
                            <td><b>Tổng kỷ luật</b></td>
                            <td>{tong_ky_luat}</td>
                        </tr>
                        <tr>
                            <td><b>Tiền bảo hiểm</b></td>
                            <td>{tien_bao_hiem}</td>
                        </tr>
                        <tr>
                            <td><b>Thực lĩnh</b></td>
                            <td><b>{thuc_linh}</b></td>
                        </tr>
                    </table>

                    <p>
                        Vui lòng kiểm tra thông tin phiếu lương. Nếu có sai lệch, Anh/Chị liên hệ
                        Phòng Nhân sự hoặc Phòng Kế toán để được hỗ trợ.
                    </p>

                    <p>Trân trọng,<br/>
                    Phòng Nhân sự - Công ty TNHH Thương mại và Dịch vụ Minh Hải</p>
                </div>
            """.format(
                nhan_vien=rec.nhan_vien_id.display_name,
                thang=rec.thang,
                nam=rec.nam,
                ma_dinh_danh=rec.ma_dinh_danh or '',
                so_ngay_cong=rec.so_ngay_cong_tinh_luong,
                luong_co_ban=rec._format_money(rec.luong_co_ban),
                phu_cap=rec._format_money(rec.phu_cap),
                tong_khen_thuong=rec._format_money(rec.tong_khen_thuong),
                tong_ky_luat=rec._format_money(rec.tong_ky_luat),
                tien_bao_hiem=rec._format_money(rec.tien_bao_hiem),
                thuc_linh=rec._format_money(rec.thuc_linh),
            )

            mail_values = {
                'subject': subject,
                'email_to': rec.email_nhan_vien,
                'body_html': body_html,
            }

            mail = self.env['mail.mail'].sudo().create(mail_values)
            mail.sudo().send()

            rec.da_gui_email = True
            rec.ngay_gui_email = fields.Datetime.now()

        return True
