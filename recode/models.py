from django.db import models
from django.contrib.auth.hashers import make_password


# --- Ruta y Subtema ---

class Ruta(models.Model):
    id_ruta = models.AutoField(primary_key=True)
    nombre_ruta = models.CharField(max_length=150)
    slug = models.SlugField(max_length=50, unique=True, default='')  # <- nuevo

    def __str__(self):
        return self.nombre_ruta


class Subtema(models.Model):
    id_subtema = models.AutoField(primary_key=True)
    nombre_subtema = models.CharField(max_length=150)
    orden = models.PositiveIntegerField(default=1)  # <- nuevo
    ruta = models.ForeignKey(
        Ruta, on_delete=models.CASCADE, related_name="subtemas", db_column="id_ruta"
    )

    class Meta:
        ordering = ["ruta", "orden"]


# --- Alumno y su progreso ---

class Alumno(models.Model):
    id_alumno = models.AutoField(primary_key=True)
    nombre_alumno = models.CharField(max_length=150)
    correo = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255)

    def set_password(self, raw_password):
        # nunca guardar la contraseña en texto plano, usar esto al crear/cambiar
        self.contrasena = make_password(raw_password)

    def __str__(self):
        return self.nombre_alumno


class ProgresoAlumno(models.Model):
    id_progreso = models.AutoField(primary_key=True)
    alumno = models.OneToOneField(Alumno, on_delete=models.CASCADE, related_name="progreso")
    puntos_exp = models.PositiveIntegerField(default=0)
    nivel = models.PositiveIntegerField(default=1)
    racha = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Progreso de {self.alumno.nombre_alumno}"


# --- Reto y sus tipos ---
# Reto es la clase base, cada tipo hereda de ella (así Django arma la
# relación 1 a 1 solo, como el triángulo del diagrama)

class Reto(models.Model):
    id_reto = models.AutoField(primary_key=True)
    subtema = models.ForeignKey(
        Subtema, on_delete=models.CASCADE, related_name="retos", db_column="id_subtema"
    )
    orden = models.PositiveIntegerField()
    recompensa_exp = models.PositiveIntegerField(default=0)
    retro_correcta = models.TextField(blank=True, default="")
    retro_incorrecta = models.TextField(blank=True, default="")
    pista = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["subtema", "orden"]
        unique_together = ("subtema", "orden")

    def __str__(self):
        return f"Reto #{self.orden} - {self.subtema.nombre_subtema}"


class RetoDD(Reto):
    # drag & drop: clasificar por categorías, ordenar algoritmo
    id_reto_dd = models.AutoField(primary_key=True)
    catalogo_dd = models.JSONField()  # ej: {"categorias": [...], "elementos": [...]}


class RetoDecision(Reto):
    # verdad/falso, selección de output, encontrar el error
    id_reto_dc = models.AutoField(primary_key=True)
    opciones_botones = models.JSONField()  # ej: {"opciones": [...], "correcta": "..."}


class RetoCifrado(Reto):
    id_reto_ci = models.AutoField(primary_key=True)
    acertijo_logico = models.JSONField()  # ej: {"mensaje_cifrado": "...", "respuesta": "..."}


class RetoCF(Reto):
    # completar frase / completar tabla
    id_reto_cf = models.AutoField(primary_key=True)
    estructura_frase = models.JSONField()  # ej: {"texto": "...", "blanks": [...]}


class ResolverReto(models.Model):
    id_resolucion = models.AutoField(primary_key=True)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name="resoluciones_reto")
    reto = models.ForeignKey(Reto, on_delete=models.CASCADE, related_name="resoluciones")
    completado_exitosamente = models.BooleanField(default=False)
    fecha_resolucion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha_resolucion"]
        # sin unique_together a propósito: se puede reintentar sin límite (CU01)

    def __str__(self):
        estado = "OK" if self.completado_exitosamente else "Fallido"
        return f"{self.alumno.nombre_alumno} - Reto {self.reto_id} ({estado})"


# --- Examen ---

class Examen(models.Model):
    id_examen = models.AutoField(primary_key=True)
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE, related_name="examenes", db_column="id_ruta")
    nombre_agente = models.CharField(max_length=150)
    tiempo_limite = models.PositiveIntegerField(help_text="segundos")
    puntaje_minimo = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre_agente


class ResolverExamen(models.Model):
    id_intento_examen = models.AutoField(primary_key=True)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name="intentos_examen")
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE, related_name="intentos")
    numero_intento = models.PositiveIntegerField(default=1)
    puntaje_obtenido = models.PositiveIntegerField(default=0)
    aprobado = models.BooleanField(default=False)
    fecha_intento = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.alumno.nombre_alumno} - {self.examen.nombre_agente} ({self.puntaje_obtenido})"


# --- Pista ---

class Pista(models.Model):
    id_pista = models.AutoField(primary_key=True)
    reto = models.ForeignKey(Reto, on_delete=models.CASCADE, related_name="pistas", db_column="id_reto")
    nombre_pista = models.CharField(max_length=150)
    definicion = models.TextField()
    costo_exp = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre_pista


class ComprarPista(models.Model):
    id_compra = models.AutoField(primary_key=True)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name="compras_pista")
    pista = models.ForeignKey(Pista, on_delete=models.CASCADE, related_name="compras")
    fecha_transaccion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.alumno.nombre_alumno} compró {self.pista.nombre_pista}"


# --- Recompensa ---

class Recompensa(models.Model):
    id_recompensa = models.AutoField(primary_key=True)
    nombre_recompensa = models.CharField(max_length=150)
    puntos_requeridos = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre_recompensa


class ReclamarRecompensa(models.Model):
    id_reclamo = models.AutoField(primary_key=True)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name="recompensas_reclamadas")
    recompensa = models.ForeignKey(Recompensa, on_delete=models.CASCADE, related_name="reclamos")
    fecha_reclamo = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("alumno", "recompensa")

    def __str__(self):
        return f"{self.alumno.nombre_alumno} reclamó {self.recompensa.nombre_recompensa}"