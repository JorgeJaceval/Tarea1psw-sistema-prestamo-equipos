import contextlib
import importlib.util
import io
import json
import logging
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

import auth
import main
import monitoreo


class MonitoreoTests(unittest.TestCase):
    def setUp(self):
        self.temporal = tempfile.TemporaryDirectory()
        self.directorio = Path(self.temporal.name) / "logs"
        self.raiz = logging.getLogger()
        self.handlers_originales = self.raiz.handlers[:]
        self.nivel_original = self.raiz.level
        self.raiz.handlers = []
        self.parches = contextlib.ExitStack()
        self.parches.enter_context(patch.object(monitoreo, "LOG_DIR", self.directorio))
        self.parches.enter_context(patch.dict("os.environ", {"SENTRY_DSN": ""}))

    def tearDown(self):
        for handler in self.raiz.handlers:
            handler.close()
        self.raiz.handlers = self.handlers_originales
        self.raiz.setLevel(self.nivel_original)
        self.parches.close()
        self.temporal.cleanup()

    def leer_log(self):
        return (self.directorio / "sistema.log").read_text(encoding="utf-8")

    def test_logs_sin_sentry_no_se_duplican_y_rotan(self):
        self.assertIsNone(monitoreo.configurar_monitoreo())
        monitoreo.configurar_monitoreo()
        self.assertEqual(len(self.raiz.handlers), 1)
        handler = self.raiz.handlers[0]
        self.assertEqual(handler.maxBytes, 1_000_000)
        self.assertEqual(handler.backupCount, 3)
        handler.maxBytes = 200
        for numero in range(20):
            logging.info("Préstamo registrado: %s", numero)
        self.assertIn("Préstamo registrado: 19", self.leer_log())
        self.assertTrue((self.directorio / "sistema.log.1").exists())
        self.assertLessEqual(len(list(self.directorio.iterdir())), 4)

    def test_sin_sdk_se_conserva_el_log_local(self):
        with patch.dict("os.environ", {"SENTRY_DSN": "https://public@example.invalid/1"}), patch.dict("sys.modules", {"sentry_sdk": None}):
            self.assertIsNone(monitoreo.configurar_monitoreo())
        logging.info("El programa sigue funcionando")
        self.assertIn("instale las dependencias", self.leer_log())
        self.assertIn("El programa sigue funcionando", self.leer_log())

    def test_login_no_registra_credenciales(self):
        monitoreo.configurar_monitoreo()
        with contextlib.redirect_stdout(io.StringIO()):
            auth.login("admin", "admin123")
            auth.login("usuario-inexistente", "clave-de-prueba")
        texto = self.leer_log()
        self.assertIn("usuario_id=1", texto)
        self.assertIn("WARNING", texto)
        for dato in ("admin123", "usuario-inexistente", "clave-de-prueba"):
            self.assertNotIn(dato, texto)

    def test_salida_normal_no_es_error_y_envia_pendientes(self):
        monitoreo.configurar_monitoreo()
        sentry = Mock()
        with patch.object(main, "configurar_monitoreo", return_value=sentry), patch.object(main, "main", side_effect=SystemExit(0)):
            with self.assertRaises(SystemExit) as salida:
                main.ejecutar()
        self.assertEqual(salida.exception.code, 0)
        sentry.flush.assert_called_once_with(timeout=2)
        self.assertIn("Cierre del sistema", self.leer_log())
        self.assertNotIn("ERROR", self.leer_log())

    def test_error_se_guarda_con_traceback_y_salida_no_exitosa(self):
        monitoreo.configurar_monitoreo()
        with patch.object(main, "configurar_monitoreo", return_value=None), patch.object(main, "main", side_effect=RuntimeError("fallo de prueba")), contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as salida:
                main.ejecutar()
        self.assertEqual(salida.exception.code, 1)
        self.assertIn("Traceback", self.leer_log())
        self.assertIn("RuntimeError: fallo de prueba", self.leer_log())

    @unittest.skipUnless(importlib.util.find_spec("sentry_sdk"), "Requiere instalar requirements.txt")
    def test_sdk_real_captura_un_error_con_contexto_sin_variables(self):
        import sentry_sdk
        eventos = []
        init_real = sentry_sdk.init

        def iniciar(**opciones):
            # Este transporte mantiene los eventos en memoria y nunca usa la red.
            return init_real(**opciones, transport=lambda evento: eventos.append(evento))

        def fallo():
            password = "secreto-local-de-prueba"
            auth.login("admin", "admin123")
            logging.warning("Contexto de prueba")
            raise RuntimeError("Fallo controlado para verificar Sentry")

        try:
            with patch.dict("os.environ", {"SENTRY_DSN": "https://public@example.invalid/1", "SENTRY_ENVIRONMENT": "pruebas"}), patch.object(sentry_sdk, "init", side_effect=iniciar), patch.object(main, "main", side_effect=fallo), contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(SystemExit):
                    main.ejecutar()
            self.assertEqual(len(eventos), 1)
            evento = eventos[0]
            self.assertEqual(evento["environment"], "pruebas")
            self.assertEqual(evento["level"], "error")
            self.assertTrue(any(miga.get("message") == "Contexto de prueba" for miga in evento["breadcrumbs"]["values"]))
            texto = json.dumps(evento)
            self.assertNotIn("admin123", texto)
            self.assertNotIn("secreto-local-de-prueba", texto)
            for excepcion in evento["exception"]["values"]:
                for frame in excepcion["stacktrace"]["frames"]:
                    self.assertFalse(frame.get("vars"))
                    self.assertFalse(frame.get("context_line"))
        finally:
            sentry_sdk.get_client().close(timeout=0)
            init_real(dsn="", default_integrations=False)

    @unittest.skipUnless(importlib.util.find_spec("sentry_sdk"), "Requiere instalar requirements.txt")
    def test_dsn_invalido_no_interrumpe_el_programa(self):
        with patch.dict("os.environ", {"SENTRY_DSN": "dsn-invalido"}):
            self.assertIsNone(monitoreo.configurar_monitoreo())
        self.assertIn("Sentry no se pudo iniciar", self.leer_log())
        self.assertNotIn("dsn-invalido", self.leer_log())


if __name__ == "__main__":
    unittest.main()
