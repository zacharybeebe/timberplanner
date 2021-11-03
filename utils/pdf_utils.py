from imports._imports_ import FPDF


class PDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font('Times', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def compile_fvs_report(self, fvs_runs, missing_no_mgt_run):
        table_width = 190
        spp_width = 50
        col_width = 20

        font_family = 'Arial'
        self.set_font(font_family, 'B', 12)
        height = 8

        self.cell(table_width, height, 'THINNING PRESCRIPTIONS', 1, 0, align='C')
        self.ln(height * 2)

        for case in fvs_runs:
            self.set_font(font_family, 'B', 10)
            if case == 'no_mgt' and missing_no_mgt_run:
                self.cell(table_width, height, 'UNABLE TO FIND "NO MANAGEMENT" SCENARIO', 0, 0, align='L')
                self.ln(height * 3)
            else:
                for key in fvs_runs[case]:
                    for sub in fvs_runs[case][key]:
                        if key == 'tables':
                            self.cell(table_width, height, sub, 0, 0, align='L')
                            self.ln(height)
                            if sub == 'DFC CONDITIONS':
                                for i, row in enumerate(fvs_runs[case][key][sub]):
                                    self.set_font(font_family, '', 9)
                                    if i in [0, 1, len(fvs_runs[case][key][sub]) - 1]:
                                        self.set_font(font_family, 'B', 9)
                                        if i == 0:
                                            self.cell(table_width, height, row, 0, 0, align='L')
                                            self.ln(height)
                                    if i != 0:
                                        for j, col in enumerate(row):
                                            if j == 0:
                                                self.cell(spp_width, height, col, 1, 0, align='L')
                                            else:
                                                if i == 1:
                                                    self.cell(col_width, height, col, 1, 0, align='C')
                                                else:
                                                    self.cell(col_width, height, str(round(col, 1)), 1, 0, align='C')
                                    self.ln(height)
                                self.ln(height * 2)
                            else:
                                for i, row in enumerate(fvs_runs[case][key][sub]):
                                    self.set_font(font_family, '', 9)
                                    if i in [0, len(fvs_runs[case][key][sub]) - 1]:
                                        self.set_font(font_family, 'B', 9)
                                    for j, col in enumerate(row):
                                        if j == 0:
                                            self.cell(spp_width, height, col, 1, 0, align='L')
                                        else:
                                            if i == 0:
                                                self.cell(col_width, height, col, 1, 0, align='C')
                                            else:
                                                self.cell(col_width, height, str(round(col, 1)), 1, 0, align='C')
                                    self.ln(height)
                                self.ln(height * 2)
                        else:
                            self.cell(spp_width, height, f'{sub}:', 0, 0, align='L')
                            self.cell(spp_width, height, fvs_runs[case][key][sub], 0, 0, align='L')
                            self.ln(height)
                    self.ln(height * 2)
                self.add_page()


