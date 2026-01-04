import os
from django.conf import settings
from django.shortcuts import render


class MaintenanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.maintenance_file = os.path.join(
            settings.BASE_DIR, "mantenimiento.txt"
        )

    def __call__(self, request):
        # Permitir admin
        if request.path.startswith("/admin"):
            return self.get_response(request)

        # Si existe el archivo → mantenimiento
        if os.path.exists(self.maintenance_file):
            return render(request, "maintenance.html", status=503)

        return self.get_response(request)
