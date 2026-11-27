from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

from progreso import servicios

from . import ejercicios

User = get_user_model()
DISPONIBLE = "batalla_final.views.final_disponible"


class BatallaFinalTests(TestCase):
    def setUp(self):
        self.alumno = User.objects.create_user("ana", password="x")
        self.client.force_login(self.alumno)

    def _responder(self, correcto):
        sesion = self.client.session["batalla_final"]
        indice = sesion["actual"]
        reto = ejercicios.RETOS[indice]
        if correcto:
            r = reto["respuesta"]
            respuesta = r[0] if reto["tipo"] == "terminal" else r
        else:
            respuesta = None
        return self.client.post(
            reverse("batalla_final:responder"),
            {"respuesta": respuesta},
            content_type="application/json",
        )

    def test_sin_examenes_no_abre(self):
        with patch(DISPONIBLE, return_value=False):
            resp = self.client.get(reverse("batalla_final:jugar"))
            self.assertRedirects(
                resp, reverse("mapa:inicio"), fetch_redirect_response=False
            )
            resp = self.client.post(reverse("batalla_final:iniciar"))
            self.assertEqual(resp.status_code, 403)

    def test_no_se_envia_la_respuesta(self):
        with patch(DISPONIBLE, return_value=True):
            resp = self.client.post(reverse("batalla_final:iniciar"))
        self.assertNotIn("respuesta", resp.json()["reto"])

    def test_vida_acierto_y_fallo(self):
        with patch(DISPONIBLE, return_value=True):
            self.client.post(reverse("batalla_final:iniciar"))
        datos = self._responder(False).json()
        self.assertEqual(datos["vida"], 100)  # no pasa de 100 %
        self.client.post(reverse("batalla_final:siguiente"))
        datos = self._responder(True).json()
        self.assertEqual(datos["vida"], 90)

    def test_victoria_marca_recode_sin_bitcoins(self):
        with patch(DISPONIBLE, return_value=True):
            self.client.post(reverse("batalla_final:iniciar"))
        datos = {}
        for _ in range(10):
            datos = self._responder(True).json()
            if datos["victoria"]:
                break
            self.client.post(reverse("batalla_final:siguiente"))
        self.assertTrue(datos["victoria"])
        self.assertTrue(servicios.reto_resuelto(self.alumno, "batalla_final:kernel"))
        self.assertEqual(servicios.obtener_progreso(self.alumno).bitcoins, 0)

    def test_abandonar_no_completa(self):
        with patch(DISPONIBLE, return_value=True):
            self.client.post(reverse("batalla_final:iniciar"))
        self.client.post(reverse("batalla_final:abandonar"))
        self.assertNotIn("batalla_final", self.client.session)
        self.assertFalse(servicios.reto_resuelto(self.alumno, "batalla_final:kernel"))

    def test_tiempo_no_se_adelanta(self):
        with patch(DISPONIBLE, return_value=True):
            self.client.post(reverse("batalla_final:iniciar"))
        resp = self.client.post(reverse("batalla_final:tiempo"))
        self.assertEqual(resp.status_code, 400)
