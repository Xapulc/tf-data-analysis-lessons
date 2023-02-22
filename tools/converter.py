import os
import fitz

from pdflatex import PDFLaTeX


class Converter(object):
    def __init__(self, tmp_dir="/tmp"):
        self.tmp_dir = tmp_dir
        os.makedirs(self.tmp_dir, exist_ok=True)

    def convert_tex_body_str_to_tex_file(self, tex_body_str):
        tex_file_path = f"{self.tmp_dir}/tmp.tex"
        with open(tex_file_path, "w+") as f:
            f.write("""
            \\documentclass[12 pt, russian]{article}
            \\usepackage[english,main=russian]{babel}
            \\begin{document}
            """)
            f.write(tex_body_str + "\n")
            f.write("""
            \\end{document}"
            """)
        return tex_file_path

    def convert_tex_file_to_pdf(self, tex_file_path):
        pdf_object = PDFLaTeX.from_texfile(tex_file_path)
        pdf, log, completed_process = pdf_object.create_pdf(keep_pdf_file=True,
                                                            keep_log_file=False)

        pdf_file_path = f"{self.tmp_dir}/tmp.pdf"
        with open(pdf_file_path, "wb") as f:
            f.write(pdf)
        return pdf_file_path

    def convert_pdf_to_image_list(self, pdf_file_path):
        res_path_list = []
        pdf_file = fitz.open(pdf_file_path)

        for i, page in enumerate(pdf_file):
            zoom = 3
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            res_path_list.append(f"{self.tmp_dir}/page_{i}.png")
            pix.save(res_path_list[-1])

        return res_path_list

    def convert_tex_body_str_to_image_list(self, tex_body_str):
        tex_file_path = self.convert_tex_body_str_to_tex_file(tex_body_str)
        pdf_file_path = self.convert_tex_file_to_pdf(tex_file_path)
        return self.convert_pdf_to_image_list(pdf_file_path)
