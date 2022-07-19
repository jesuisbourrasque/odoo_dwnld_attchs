import base64
from io import BytesIO
from zipfile import ZipFile
from odoo import http


class DownloadZipFile(http.Controller):
    @http.route("/download_attachments/", type="http", auth="user", website=True)
    def download_attachments_product_routes(self, **data):
        attachments_items = http.request.env["ir.attachment"].search(
            [("res_id", "=", data.get("res_id")), ("res_model", "=", "department.plan")])
        in_memory = BytesIO()
        zip_archive = ZipFile(in_memory, "w")
        for attachment in attachments_items:
            zip_archive.writestr(attachment.name, base64.b64decode(attachment.datas))
        zip_archive.close()
        res = http.send_file(in_memory, filename="attachments.zip", as_attachment=True)
        return res
