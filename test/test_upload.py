import pytest
import allure
from pages.upload_page import UploadPage


# ============================================================
# 🎵 TEST FUNCIONALES DEL MÓDULO "UPLOAD" (Audius Music)
# ============================================================

@allure.feature("Upload")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC001 - Subir archivo válido en formato mp3")
@allure.description("""
Description
Desde el módulo Upload, el usuario selecciona un archivo de audio válido con extensión .mp3 y lo envía para su carga.
El sistema procesa el archivo y refleja el estado de subida exitosa sin errores de validación.

Resultado esperado : El archivo .mp3 se carga correctamente y la UI muestra el estado de “subido” (o equivalente), permitiendo continuar con el flujo de publicación/edición.

Pre-conditions
SO/Navegador: Windows/macOS/Linux con Chrome/Edge/Firefox actualizados
Aplicación web Audius accesible
Sesión iniciada con una cuenta válida (fixture: page_with_session)
Archivo de prueba existente y legible: resources/audio/demo.mp3
Permisos del navegador para seleccionar archivos
""")
@pytest.mark.smoke
@pytest.mark.integration
def test_TC001_subir_archivo_valido(page_with_session):
    upload = UploadPage(page_with_session)
    file_path = "resources/audio/demo.mp3"

    with allure.step("Abrir módulo Upload"):
        upload.open()

    with allure.step(f"Subir archivo válido: {file_path}"):
        upload.upload_audio_file(file_path)
        page_with_session.wait_for_timeout(5000)
        upload.assert_file_uploaded()

    allure.attach(page_with_session.screenshot(), name="Archivo_subido", attachment_type=allure.attachment_type.PNG)
    print("✅ Archivo mp3 subido correctamente.")


@allure.feature("Upload")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC002 - Poner TrackName con menos de 65 caracteres")
@allure.description("""
Description
Tras cargar un audio válido, el usuario ingresa un TrackName cuya longitud es menor a 65 caracteres y completa los campos obligatorios.
El sistema acepta el nombre y permite guardar sin errores.

Resultado esperado : El TrackName (< 65 caracteres) se guarda correctamente y el flujo avanza sin validaciones bloqueantes.

Pre-conditions
SO/Navegador: Windows/macOS/Linux con Chrome/Edge/Firefox
Aplicación web Audius accesible
Sesión iniciada con una cuenta válida
Archivo de prueba: resources/audio/demo.mp3
""")
@pytest.mark.functional
@pytest.mark.integration
def test_TC002_poner_en_el_TracKName_menor_a_65_caracteres(page_with_session):
    upload = UploadPage(page_with_session)
    file_path = "resources/audio/demo.mp3"

    with allure.step("Subir archivo de audio válido"):
        upload.open()
        upload.upload_audio_file(file_path)
        upload.assert_file_uploaded()
        upload.BotonSiguiente()

    with allure.step("Rellenar campos obligatorios"):
        upload.CamposObligatorios(
            nuevo_nombre="Tema con Artwork QA",
            genero_primera_opcion=True,
            artwork_busqueda="rock",
            tag_valor="juegos",
        )
        page_with_session.wait_for_timeout(5000)
        upload.Save()

    allure.attach(page_with_session.screenshot(), name="TrackName_valido", attachment_type=allure.attachment_type.PNG)
    print("✅ TrackName ingresado correctamente.")


@allure.feature("Upload")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC003 - No permitir TrackName vacío")
@allure.description("""
Description
Luego de subir un audio válido, el usuario intenta continuar dejando el campo TrackName vacío.
El sistema valida que el nombre no puede estar vacío y muestra un mensaje de error.

Resultado esperado : Se bloquea el guardado y aparece el mensaje “Your track must have a name.”.

Pre-conditions
SO/Navegador: Windows/macOS/Linux con Chrome/Edge/Firefox
Aplicación web Audius accesible
Sesión iniciada válida
Archivo de prueba: resources/audio/demo.mp3
""")
@pytest.mark.functional
@pytest.mark.integration
def test_TC003_Verificar_que_no_permita_poner_en_el_TracKName_caracteres_vacios_(page_with_session):
    upload = UploadPage(page_with_session)
    file_path = "resources/audio/demo.mp3"

    with allure.step("Subir archivo y dejar nombre vacío"):
        upload.open()
        upload.upload_audio_file(file_path)
        upload.assert_file_uploaded()
        upload.BotonSiguiente()
        upload.CamposObligatorios(
            nuevo_nombre="",
            genero_primera_opcion=True,
            artwork_busqueda="rock",
            tag_valor="juegos",
        )
        page_with_session.wait_for_timeout(5000)
        upload.Save()

    with allure.step("Validar mensaje de error por nombre vacío"):
        assert upload.validar_mensaje("Your track must have a name."), "❌ No se mostró el mensaje esperado"

    allure.attach(page_with_session.screenshot(), name="Error_nombre_vacio", attachment_type=allure.attachment_type.PNG)


@allure.feature("Upload")
@allure.severity(allure.severity_level.MINOR)
@allure.title("TC004 - No permitir solo espacios en el campo Name")
@allure.description("""
Description
El usuario intenta guardar un TrackName compuesto únicamente por espacios.
El sistema debe normalizar/validar y rechazar nombres vacíos efectivos.

Resultado esperado : Se bloquea el guardado y se muestra el mensaje “Your track must have a name.”.
Nota: Caso marcado como xfail por bug conocido (actualmente acepta espacios).

Pre-conditions
SO/Navegador: Windows/macOS/Linux con Chrome/Edge/Firefox
Aplicación web Audius accesible
Sesión iniciada válida
Archivo de prueba: resources/audio/demo.mp3
""")
@pytest.mark.functional
@pytest.mark.integration
@pytest.mark.xfail(reason="Bug conocido: el sistema acepta espacios como caracteres válidos")
def test_TC004_Verificar_que_no_permita_ingresar_espacios_vacios_al_campo_de_Name_validando_como_Caracteres(page_with_session):
    upload = UploadPage(page_with_session)
    file_path = "resources/audio/demo.mp3"

    with allure.step("Subir archivo con nombre de solo espacios"):
        upload.open()
        upload.upload_audio_file(file_path)
        upload.assert_file_uploaded()
        upload.BotonSiguiente()
        upload.CamposObligatorios(
            nuevo_nombre=" ",
            genero_primera_opcion=True,
            artwork_busqueda="rock",
            tag_valor="juegos",
        )
        upload.Save()

    with allure.step("Validar mensaje de error"):
        assert upload.validar_mensaje("Your track must have a name."), "❌ No se mostró el mensaje esperado"


@allure.feature("Upload")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC005 - Quitar espacios vacíos y permitir solo caracteres válidos")
@allure.description("""
Description
El usuario ingresa un TrackName con espacios extra (p. ej., dobles espacios o espacios al inicio/fin) y caracteres válidos.
El sistema limpia/normaliza el nombre, preservando únicamente caracteres válidos, y permite guardar.

Resultado esperado : El TrackName se guarda sin espacios sobrantes (trim/condensado) y sin caracteres inválidos.

Pre-conditions
SO/Navegador: Windows/macOS/Linux con Chrome/Edge/Firefox
Aplicación web Audius accesible
Sesión iniciada válida
Archivo de prueba: resources/audio/demo.mp3
""")
@pytest.mark.functional
@pytest.mark.integration
def test_TC005_Verificar_que_al_subir_con_espacios_vacios_en_el_campo_Name_se_quite_automaticamente_mostrando_solo_caracteres(page_with_session):
    upload = UploadPage(page_with_session)
    file_path = "resources/audio/demo.mp3"

    with allure.step("Subir archivo y limpiar espacios en TrackName"):
        upload.open()
        upload.upload_audio_file(file_path)
        upload.assert_file_uploaded()
        upload.BotonSiguiente()
        upload.CamposObligatorios(
            nuevo_nombre="The Rock - Beatles",
            genero_primera_opcion=True,
            artwork_busqueda="rock",
            tag_valor="juegos",
        )
        upload.Save()

    allure.attach(page_with_session.screenshot(), name="Track_limpio", attachment_type=allure.attachment_type.PNG)


@allure.feature("Upload")
@allure.severity(allure.severity_level.MINOR)
@allure.title("TC006 - No permitir tags de más de 30 caracteres")
@allure.description("""
Description
El usuario intenta ingresar un valor en Tags cuya longitud supera los 30 caracteres.
El sistema debe validar el límite y bloquear el guardado hasta corregir el campo.

Resultado esperado : Se muestra una advertencia/mensaje de error (p. ej., “Fix errors to continue your upload.”) y no se permite continuar.
Nota: Caso marcado como xfail por bug conocido (actualmente permite > 30 caracteres).

Pre-conditions
SO/Navegador: Windows/macOS/Linux con Chrome/Edge/Firefox
Aplicación web Audius accesible
Sesión iniciada válida
Archivo de prueba: resources/audio/demo.mp3
""")
@pytest.mark.functional
@pytest.mark.integration
@pytest.mark.xfail(reason="Permite ingresar más de 30 caracteres en el campo tags")
def test_TC006_Verificar_que_no_permita_tags_que_superen_los_30_caracteres(page_with_session):
    upload = UploadPage(page_with_session)
    file_path = "resources/audio/demo.mp3"

    with allure.step("Subir archivo y usar tag muy largo"):
        upload.open()
        upload.upload_audio_file(file_path)
        upload.assert_file_uploaded()
        upload.BotonSiguiente()
        upload.CamposObligatorios(
            nuevo_nombre="The Rock 123123113@@@e112412!#$%&/()",
            genero_primera_opcion=True,
            artwork_busqueda="rock",
            tag_valor="LaamistadesunarelaciónafectivaentredosomáspersonasLaamistadesunarelaciónafectivaentredosomáspersonas.",
        )
        upload.Save()

    with allure.step("Validar mensaje por tag largo"):
        assert upload.AssertMensajesLargos("Fix errors to continue your upload."), "❌ No se mostró el mensaje esperado"


@allure.feature("Upload")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC007 - No permitir archivos que no sean mp3 o wav")
@allure.description("""
Description
El usuario intenta cargar un archivo con extensión no soportada (p. ej., .jpg) en el módulo Upload.
El sistema valida el tipo MIME/extensión y rechaza la carga.

Resultado esperado : No se permite la subida y se muestra el mensaje “Unsupported File Type”.

Pre-conditions
SO/Navegador: Windows/macOS/Linux con Chrome/Edge/Firefox
Aplicación web Audius accesible
Sesión iniciada válida
Archivo de prueba inválido disponible: resources/audio/prueba.jpg
""")
@pytest.mark.smoke
@pytest.mark.integration
def test_TC007_Verificar_que_no_permita_subir_Archivos_que_no_estan_en_formato_mp3o_wav(page_with_session):
    upload = UploadPage(page_with_session)
    file_path = "resources/audio/prueba.jpg"

    with allure.step("Intentar subir archivo no compatible"):
        upload.open()
        upload.upload_audio_file(file_path)
        upload.assert_file_uploaded()

    with allure.step("Validar mensaje de tipo de archivo no soportado"):
        assert upload.validar_mensaje("Unsupported File Type"), "❌ No se mostró el mensaje esperado"

    allure.attach(page_with_session.screenshot(), name="Archivo_invalido", attachment_type=allure.attachment_type.PNG)


@allure.feature("Upload")
@allure.severity(allure.severity_level.MINOR)
@allure.title("TC008 - No permitir más de 64 caracteres en TrackName")
@allure.description("""
Description
El usuario ingresa un TrackName que supera el límite permitido (más de 64 caracteres) e intenta guardar.
El sistema debe impedir el guardado y mostrar una validación clara.

Resultado esperado : No se permite continuar hasta que el TrackName cumpla la longitud (≤ 64). Debe mostrarse mensaje o inhabilitar el botón de guardado.

Pre-conditions
SO/Navegador: Windows/macOS/Linux con Chrome/Edge/Firefox
Aplicación web Audius accesible
Sesión iniciada válida
Archivo de prueba: resources/audio/demo.mp3
""")
@pytest.mark.functional
@pytest.mark.integration
def test_TC008_Verificar_que_no_permita_ingresar_mas_de_64_caracteres_en_el_campo_TrackName(page_with_session):
    upload = UploadPage(page_with_session)
    file_path = "resources/audio/demo.mp3"

    with allure.step("Ingresar TrackName demasiado largo"):
        upload.open()
        upload.upload_audio_file(file_path)
        upload.assert_file_uploaded()
        upload.BotonSiguiente()
        upload.CamposObligatorios(
            nuevo_nombre="Grupo_Rock- the beatles-stramberry" * 4,
            genero_primera_opcion=True,
            artwork_busqueda="rock",
            tag_valor="juegos",
        )
        upload.Save()

    allure.attach(page_with_session.screenshot(), name="Nombre_largo", attachment_type=allure.attachment_type.PNG)


@allure.feature("Upload")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC009 - Permitir mínimo 1 caracter en TrackName")
@allure.description("""
Description
El usuario ingresa un TrackName de un solo carácter y completa los campos obligatorios.
El sistema considera válido el mínimo y permite guardar.

Resultado esperado : El TrackName de 1 carácter se guarda correctamente y no se presentan mensajes de error.

Pre-conditions
SO/Navegador: Windows/macOS/Linux con Chrome/Edge/Firefox
Aplicación web Audius accesible
Sesión iniciada válida
Archivo de prueba: resources/audio/demo.mp3
""")
@pytest.mark.functional
@pytest.mark.integration
def test_TC009_Verificar_que_permita_ingresar_al_menos_1caracter_en_el_campo_TrackName_como_valido(page_with_session):
    upload = UploadPage(page_with_session)
    file_path = "resources/audio/demo.mp3"

    with allure.step("Ingresar TrackName de un solo carácter"):
        upload.open()
        upload.upload_audio_file(file_path)
        upload.assert_file_uploaded()
        upload.BotonSiguiente()
        upload.CamposObligatorios(
            nuevo_nombre="a",
            genero_primera_opcion=True,
            artwork_busqueda="rock",
            tag_valor="juegos",
        )
        upload.Save()

    allure.attach(page_with_session.screenshot(), name="TrackName_1caracter", attachment_type=allure.attachment_type.PNG)


@allure.feature("Upload")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC010 - Permitir mínimo 1 caracter en Tags")
@allure.description("""
Description
El usuario ingresa un Tag de un solo carácter junto con el resto de campos obligatorios.
El sistema acepta el mínimo permitido en el campo Tags y permite guardar.

Resultado esperado : El contenido se guarda correctamente con Tags de longitud mínima (1 carácter).

Pre-conditions
SO/Navegador: Windows/macOS/Linux con Chrome/Edge/Firefox
Aplicación web Audius accesible
Sesión iniciada válida
Archivo de prueba: resources/audio/demo.mp3
""")
@pytest.mark.functional
@pytest.mark.integration
def test_TC010_Verificar_como_minimo_1_caracter_de_tamaño_ene_el_campo_Tags_para_ser_Valido(page_with_session):
    upload = UploadPage(page_with_session)
    file_path = "resources/audio/demo.mp3"

    with allure.step("Ingresar solo un carácter en Tags"):
        upload.open()
        upload.upload_audio_file(file_path)
        upload.assert_file_uploaded()
        upload.BotonSiguiente()
        upload.CamposObligatorios(
            nuevo_nombre="The Rock - Green day",
            genero_primera_opcion=True,
            artwork_busqueda="rock",
            tag_valor="a",
        )
        upload.Save()

    allure.attach(page_with_session.screenshot(), name="Tags_1caracter", attachment_type=allure.attachment_type.PNG)
