from playwright.sync_api import Page, Locator, expect
from config.settings import UPLOAD_URL
from pathlib import Path
import re


class UploadPage:
    def __init__(self, page: Page):
        self.page = page
        # === LOCATORS ===
        self.title = page.get_by_role("heading", name="Upload Your Music")
        self.browse_link: Locator = page.locator('a', has_text="browse to upload")  # linkText
        self.file_input: Locator = page.locator('//input[@type="file"]')            # tu XPath
        self.processing_msg: Locator = page.locator('text=Continue Uploading')
        self.next_button: Locator = page.locator('button:has-text("Next")')
        self.continue_btn = page.get_by_role("button", name="Continue")  ##boton de siguiente
        self.track_title = page.locator("input[name='trackMetadatas.0.title']") #campo de track Name
        self.final_upload_btn = page.get_by_role("button", name="Complete Upload") #Boton de Subir cancion
        self.track_name_input = self.page.locator("//input[@value='rock']")
        self.genre_required_msg = self.page.locator("span.harmony-1iumh44", has_text="Genre is required.")

    
        # Triggers posibles del Select (cualquiera que tengas disponible)
        self.genre_combobox_by_role = page.get_by_role("combobox", name=re.compile(r"pick a genre", re.I))
        self.genre_trigger_css = page.locator("css=._query_1jpe6_41 > input")
        self.genre_input_antd = page.locator("input.ant-select-selection-search-input[role='combobox']")
        # Panel visible del dropdown de Ant Design (rc-select)
        self.dropdown_panel = page.locator(".ant-select-dropdown:not(.ant-select-dropdown-hidden)").last
    
    def _locators_artwork(self):
        # Botón / texto para abrir sección de artwork
        add_artwork_btn = self.page.get_by_text(re.compile(r"^\s*Add Artwork\s*$", re.I))

        # Opción "Find Artwork" dentro del flujo de artwork
        find_artwork_btn = self.page.get_by_text(re.compile(r"^\s*Find Artwork\s*$", re.I))

        # Input de búsqueda por placeholder
        search_input = self.page.locator("input[placeholder='Search Images']")

        # Botón buscar (por nombre visible y/o clase)
        search_btn = self.page.get_by_role("button", name=re.compile(r"^\s*Search\s*$", re.I))
        if not search_btn.count():
            search_btn = self.page.locator("button.harmony-6qmhv8", has_text=re.compile(r"^\s*Search\s*$", re.I))

        # Contenedor de resultados (portal/modal). AntD suele montar un overlay:
        # tomamos algo amplio y seleccionamos la 1ª imagen visible adentro.
        results_scope = self.page.locator("body")
        first_result_img = results_scope.locator("img, [role='img']").first

        # (Opcional) A veces hay botón "Select" o similar tras elegir la imagen
        select_btn = self.page.get_by_role("button", name=re.compile(r"^\s*Select\s*$", re.I))

        return add_artwork_btn, find_artwork_btn, search_input, search_btn, first_result_img, select_btn

    def _locator_tag_input(self):
        # Campo de tags que mencionaste: css=._newTagInput_1mktd_76
        return self.page.locator("css=._newTagInput_1mktd_76")
    def agregar_artwork_por_busqueda(self, consulta: str = "rock"):
        """
        Abre 'Add Artwork' -> 'Find Artwork' -> busca 'consulta' -> selecciona el 1er resultado.
        """
        add_artwork_btn, find_artwork_btn, search_input, search_btn, first_result_img, select_btn = self._locators_artwork()

        # 1) Abrir flujo de artwork
        expect(add_artwork_btn).to_be_visible(timeout=15000)
        add_artwork_btn.click()

        expect(find_artwork_btn).to_be_visible(timeout=10000)
        find_artwork_btn.click()

        # 2) Buscar por texto
        expect(search_input).to_be_visible(timeout=10000)
        search_input.fill("")          # limpia
        search_input.type(consulta)    # escribe consulta (p.ej. "rock")

        expect(search_btn).to_be_visible(timeout=10000)
        search_btn.click()

        # 3) Seleccionar primer resultado visible
        # Espera breve a que lleguen las imágenes
        self.page.wait_for_timeout(800)
        expect(first_result_img).to_be_visible(timeout=10000)
        first_result_img.scroll_into_view_if_needed()
        first_result_img.click()

        # 4) Confirmar selección si existe botón 'Select' (no todas las UIs lo requieren)
        if select_btn.count():
            try:
                expect(select_btn).to_be_enabled(timeout=3000)
                select_btn.click()
            except Exception:
                # Si no está o no hace falta, continúa sin bloquear
                pass

        # Pausa breve para que se refleje el artwork en el UI
        self.page.wait_for_timeout(600)
    def agregar_tag(self, valor: str = "juegos"):
        """
        En el campo de tags (._newTagInput_1mktd_76), escribe el valor y confirma (Enter).
        """
        tag_input = self._locator_tag_input()
        expect(tag_input).to_be_visible(timeout=10000)
        tag_input.click()
        tag_input.fill("")
        tag_input.type(valor)
        tag_input.press("Enter")
        # Opcional: pequeña pausa para que aparezca el chip/tag
        self.page.wait_for_timeout(300)

    def open(self):
        self.page.goto(UPLOAD_URL)
        expect(self.title).to_be_visible(timeout=10000)

    def _open_genre_dropdown(self):
        """Abre el dropdown del Select (Antd) y espera el panel visible."""
        opened = False
        for trigger in (self.genre_combobox_by_role, self.genre_trigger_css, self.genre_input_antd):
            if trigger.count():
                trigger.click(force=True)
                try:
                    expect(self.dropdown_panel).to_be_visible(timeout=2000)
                    opened = True
                    break
                except AssertionError:
                    # intenta otro trigger
                    pass

        if not opened:
            # último recurso: click en el primer combobox visible y Enter
            cb = self.page.locator("[role='combobox']").first
            cb.click(force=True)
            self.page.keyboard.press("Enter")
            expect(self.dropdown_panel).to_be_visible(timeout=5000)

    def _select_first_genre(self):
        """
        Selecciona la PRIMERA opción visible y no deshabilitada del panel.
        Fallback por teclado si el click no funciona.
        """
        # Asegura panel visible
        expect(self.dropdown_panel).to_be_visible(timeout=5000)

        # Primera opción visible no deshabilitada dentro del panel ABIERTO
        first_option = self.dropdown_panel.locator(
            "[role='option']:not([aria-disabled='true'])"
        ).first

        # A veces Antd pinta opciones pero con hidden: espera visibilidad real
        try:
            expect(first_option).to_be_visible(timeout=3000)
            first_option.scroll_into_view_if_needed()
            first_option.click()
        except AssertionError:
            # Fallback por teclado (Antd lo soporta muy bien)
            self.page.keyboard.press("ArrowDown")
            self.page.keyboard.press("Enter")

    def click_browse_link(self):
        """Hace clic en el enlace 'browse to upload'."""
        expect(self.browse_link).to_be_visible(timeout=8000)
        self.browse_link.click()
        print("🖱️ Clic en 'browse to upload' realizado correctamente.")

    def upload_audio_file(self, file_path: str):
        """Selecciona un archivo de audio válido (mp3, wav, flac, etc.)."""
        expect(self.file_input).to_be_visible(timeout=8000)
        self.file_input.set_input_files(file_path)
        print(f"🎵 Archivo '{file_path}' cargado correctamente.")

    def assert_file_uploaded(self):
        """Verifica que el archivo fue detectado (Processing o Next visible)."""
        expect(self.processing_msg.or_(self.next_button)).to_be_visible(timeout=15000)
        print("✅ Archivo procesado y detectado correctamente.")

    def BotonSiguiente(self):
        expect(self.continue_btn).to_be_visible(timeout=20000)
        self.continue_btn.click()

    def CamposObligatorios(self, nuevo_nombre: str, genero_primera_opcion: bool = True,
                                    artwork_busqueda: str | None = "rock", tag_valor: str | None = "juegos"):
        
        expect(self.track_title).to_be_visible(timeout=20000)
        self.track_title.fill("")                # limpia campo existente
        self.track_title.type(nuevo_nombre)      # escribe el nuevo título

        # 2) Abrir Select y elegir primera opción
        self._open_genre_dropdown()
        self._select_first_genre()
        self.page.wait_for_timeout(300)  # deja que el chip/valor se refleje
        # 4) Tag (opcional)
        self.page.wait_for_timeout(1500)
        try:
            # clic neutro para descartar cualquier modal flotante
            self.page.mouse.click(10, 10)
            print("🧩 Modal inicial cerrado con clic neutro.")
        except Exception:
            pass

        if tag_valor:
            self.agregar_tag(tag_valor)

        # 5) Artwork por búsqueda (opcional)
        if artwork_busqueda:
            self.agregar_artwork_por_busqueda(artwork_busqueda)
        try:
            # clic neutro para descartar cualquier modal flotante
            self.page.mouse.click(10, 10)
            print("🧩 Modal inicial cerrado con clic neutro.")
        except Exception:
            pass
    
    def Save(self):
  
        # 1️⃣ Clic en el botón principal "Upload"
        expect(self.final_upload_btn).to_be_visible(timeout=20000)
        self.final_upload_btn.click()

        # 2️⃣ Espera a que aparezca el modal de confirmación
        modal_upload_btn = self.page.locator("button.harmony-1p95fbe", has_text="Upload")

        try:
            expect(modal_upload_btn).to_be_visible(timeout=10000)
            modal_upload_btn.click()  # confirma en el modal
        except Exception:
            print("⚠️ No se detectó modal de confirmación, continuando...")

        # 3️⃣ Espera unos segundos para ver el resultado o proceso final
        self.page.wait_for_timeout(5000)

    def validar_mensaje(self, texto: str, timeout=5000) -> bool:
   
        try:
            locator = self.page.locator(f"text={texto}")
            expect(locator).to_be_visible(timeout=timeout)
            print(f"✅ Mensaje visible: '{texto}'")
            return True
        except Exception:
            print(f"❌ No se encontró el mensaje: '{texto}'")
            return False
        
    def AssertMensajesLargos(self, texto: str, timeout=5000) -> bool:
   
        try:
            locator = self.page.locator(f"text={texto}")
            expect(locator).to_be_visible(timeout=timeout)
            print(f"✅ Mensaje visible: '{texto}'")
            return True
        except Exception:
            print(f"❌ No se encontró el mensaje: '{texto}'")
            return False