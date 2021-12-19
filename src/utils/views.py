from typing import List

import tabula
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import FormView, TemplateView
from pandas.core.frame import DataFrame

from utils.forms import RakutenForm


class UtilListView(TemplateView):
    template_name = "utils/index.html"


class QRCodeGeneratorView(TemplateView):
    template_name = "utils/qrcode.html"


class MarkdownEditorView(TemplateView):
    template_name = "utils/markdown.html"


class RakutenConverterView(FormView):
    template_name = "utils/rakuten.html"
    form_class = RakutenForm
    table_headers = ["利用日", "利用店名", "利用者", "支払方法", "利用金額", "手数料", "支払総額", "当月請求額", "翌月繰越残高"]

    def form_valid(self, form: RakutenForm):
        file = self.request.FILES["pdf"]
        tables: List[DataFrame] = tabula.read_pdf(file, lattice=True, pages="all")
        result_table = DataFrame()
        for table in tables:
            if not list(table.columns) == self.table_headers:
                continue
            result_table = result_table.append(table)
        if len(result_table):
            response = HttpResponse(content_type="text/csv")
            filename = "rakuten.csv"
            response["Content-Disposition"] = f"attachment; filename={filename}"
            result_table = result_table[["利用日", "利用店名", "利用金額"]].dropna()
            result_table["利用金額"] = result_table["利用金額"].dropna().astype(str).str.replace(",", "").astype(int)
            response.write(result_table.sort_values("利用日").to_csv(index=False))
        else:
            response = HttpResponseRedirect(reverse("utils_rakuten"))
        return response


class CSVTOMDConvertorView(TemplateView):
    template_name = "utils/csv_to_md.html"


class MUFJDebitConverterView(FormView):
    template_name = "utils/mufj_debit.html"
    form_class = RakutenForm

    def form_valid(self, form: RakutenForm):
        file = self.request.FILES["pdf"]
        tables: List[DataFrame] = tabula.read_pdf(file, lattice=False, pages="all")
        result_table = DataFrame()
        for table in tables:
            if not list(table.columns)[0] == "お取引日 お取引内容":
                continue
            table[["お取引日", "お取引内容"]] = table["お取引日 お取引内容"].str.split(n=1, expand=True)
            table = table.dropna(subset=["お取引日", "お取引内容", "ご利用額"]).rename(
                columns={"お取引日": "利用日", "お取引内容": "利用店名", "ご利用額": "利用金額"}
            )
            result_table = result_table.append(table[["利用日", "利用店名", "利用金額"]])
        if len(result_table):
            response = HttpResponse(content_type="text/csv")
            filename = "mufj.csv"
            response["Content-Disposition"] = f"attachment; filename={filename}"
            result_table["利用金額"] = result_table["利用金額"].astype(str).str.replace(",", "").astype(int)
            response.write(result_table.sort_values("利用日").to_csv(index=False))
        else:
            response = HttpResponseRedirect(reverse("utils_mufj_debit"))
        return response
