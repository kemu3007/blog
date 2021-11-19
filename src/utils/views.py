from django.views.generic import TemplateView


class UtilListView(TemplateView):
    template_name = "utils/index.html"


class QRCodeGeneratorView(TemplateView):
    template_name = "utils/qrcode.html"
