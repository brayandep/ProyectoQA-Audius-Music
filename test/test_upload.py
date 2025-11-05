import pytest
import allure
from pages.upload_page import UploadPage


# ============================================================
# 🎵 TEST FUNCIONALES DEL MÓDULO "UPLOAD" (Audius Music)
# ============================================================

@allure.feature("Upload")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC001 - Subir archivo válido en formato mp3")
@pytest.mark.functional
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
@pytest.mark.functional
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
@pytest.mark.functional
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
@pytest.mark.functional
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
@pytest.mark.functional
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
@pytest.mark.functional
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
@pytest.mark.functional
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
@pytest.mark.functional
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
@pytest.mark.functional
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
@pytest.mark.functional
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
