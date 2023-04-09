import os
import fitz

from pdflatex import PDFLaTeX


class Converter(object):
    def __init__(self, tmp_dir=None):
        if tmp_dir is None:
            current_path = os.path.dirname(os.path.dirname(__file__))
            self.tmp_dir = os.path.join(current_path, "tmp/")
        else:
            self.tmp_dir = tmp_dir

        os.makedirs(self.tmp_dir, exist_ok=True)

    def convert_tex_body_str_to_tex_file(self, tex_body_str):
        tex_file_path = os.path.join(self.tmp_dir, "tmp.tex")
        with open(tex_file_path, "w+") as f:
            f.write(r"""
            \documentclass[12 pt, russian]{article}
            \usepackage[english,main=russian]{babel}
            
            \usepackage[T1]{fontenc}
            \usepackage[utf8]{luainputenc}
            \usepackage{geometry}
            \usepackage[pdftex]{graphicx}
            \usepackage{amstext}
            \usepackage{amssymb}
            \usepackage{amsmath}
            \usepackage{amsthm}
            \usepackage{mathrsfs} 
            \usepackage[T1,T2A]{fontenc}
            \usepackage[utf8]{inputenc}
            \usepackage{listings}
            \usepackage{xcolor}
            
            \definecolor{codegreen}{rgb}{0,0.6,0}
            \definecolor{codegray}{rgb}{0.5,0.5,0.5}
            \definecolor{codepurple}{rgb}{0.58,0,0.82}
            \definecolor{backcolour}{rgb}{0.95,0.95,0.92}
            
            \lstdefinestyle{mystyle}{
                backgroundcolor=\color{backcolour},   
                commentstyle=\color{codegreen},
                keywordstyle=\color{magenta},
                numberstyle=\tiny\color{codegray},
                stringstyle=\color{codepurple},
                basicstyle=\ttfamily\footnotesize,
                breakatwhitespace=false,         
                breaklines=true,                 
                captionpos=b,                    
                keepspaces=true,                 
                numbers=left,                    
                numbersep=5pt,                  
                showspaces=false,                
                showstringspaces=false,
                showtabs=false,                  
                tabsize=2
            }
            
            \lstset{style=mystyle}
            \begin{document}
            """)
            f.write(tex_body_str + "\n")
            f.write(r"""
            \end{document}
            """)
        return tex_file_path

    def convert_tex_file_to_pdf(self, tex_file_path):
        pdf_object = PDFLaTeX.from_texfile(tex_file_path)
        pdf, log, completed_process = pdf_object.create_pdf(keep_pdf_file=True,
                                                            keep_log_file=False)

        pdf_file_path = os.path.join(self.tmp_dir, "tmp.pdf")
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
            res_path_list.append(os.path.join(self.tmp_dir, f"page_{i}.png"))
            pix.save(res_path_list[-1])

        return res_path_list

    def convert_tex_body_str_to_image_list(self, tex_body_str):
        tex_file_path = self.convert_tex_body_str_to_tex_file(tex_body_str)
        pdf_file_path = self.convert_tex_file_to_pdf(tex_file_path)
        return self.convert_pdf_to_image_list(pdf_file_path)
