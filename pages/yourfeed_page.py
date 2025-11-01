# pages/yourfeed_page.py
from playwright.sync_api import Page, Locator, expect, TimeoutError as PlaywrightTimeoutError
from config.settings import FEED_URL
from playwright_helpers.locators import (
    by_testid, has_testid, has_class, attr_contains, any_of, text_exact, text_like
)


class YourFeedPage:
    def __init__(self, page: Page):
        self.page = page
        self.page.set_default_timeout(10000)  # timeout base para todas las esperas

        # ==== LOCATORS (robustos y centralizados) ====

        # Título principal del feed
        self.title: Locator = page.locator(text_exact("Your Feed"))

        # Tarjeta (track)
        self.card: Locator = page.locator(
            any_of(
                #by_testid("trackTile"), 
                has_class("artworkWrapper"))
        ).first
        #imagen dentro de tarjeta
        self.card_artwork = self.card.locator(
            any_of(
            has_class("artwork"),
            has_testid("dynamic-image-first"),
            has_testid("dynamic-image-second")
         )
        ).first

        # Botón Play / Pause (el SVG con <title>Play/Pause)
        self.card_play_btn = self.card.locator(
           any_of(
            has_class("artworkIcon"),
            "svg >> text=/^(Play|Pause)$/"
              )
        ).first

        # Repost / Favorite en la tarjeta
        self.repost_button: Locator = page.locator(
            any_of(has_testid("repost"), attr_contains("aria-label", "Repost"))
        ).first
        self.favorite_button: Locator = page.locator(
            any_of(has_testid("favorite"), attr_contains("aria-label", "Favorite"))
        ).first

        # Menú "más opciones"
        self.more_options_button: Locator = page.locator(
            any_of(
                attr_contains("aria-label", "More options"),
                has_testid("more"),
                "button:has(svg)"
            )
        ).first

        # Opciones del menú desplegable
        self.add_playlist_option: Locator   = page.locator(text_exact("Add to Playlist"))
        self.new_playlist_option: Locator   = page.locator(text_exact("New Playlist"))
        self.share_option: Locator          = page.locator(text_exact("Share"))
        self.direct_message_option: Locator = page.locator(text_exact("Direct Message"))
        self.embedded_option: Locator       = page.locator(text_exact("Embed"))
        self.copy_link_option: Locator      = page.locator(text_exact("Copy Link"))

        # Elementos/feedback tras acciones
        self.mini_player: Locator = page.locator(
            any_of(has_class("_playBarControls_1o5hm_30"))
            #any_of(by_testid("playerBar"), has_class("_playBarControls_1o5hm_30"), has_class("playBar"))
        )
        # Botones de estado del mini-player (scoped al mini_player)
        self.mini_play_btn  = self.mini_player.locator(
         any_of(has_testid("play"), attr_contains("aria-label", "Play"), has_class("play"))
            ).first
        self.mini_pause_btn = self.mini_player.locator(
            any_of(attr_contains("aria-label", "pause track"))
          #any_of(has_testid("pause"), attr_contains("aria-label", "pause track"), has_class("pause"))
        ).first


        self.confirm_toast: Locator = page.locator(
            any_of(
                has_class("toast"),
                '[role="status"]',
                text_like("copied|added|playlist|saved")
            )
        )
        self.embed_modal: Locator = page.locator('[role="dialog"]').filter(
            has=page.locator(text_exact("Embed"))
        )
        self.search_dm: Locator = page.locator(
            any_of(attr_contains("placeholder", "Search"), attr_contains("aria-label", "Search"))
        )

        # === Modal de notificaciones ===
        self.modal_title = page.locator('text="DON\'T MISS A THING!"')
        self.modal_dialog = page.locator('[role="dialog"]')
        self.maybe_later_btn = page.get_by_role("button", name="MAYBE LATER")
        self.enable_btn     = page.get_by_role("button", name="ENABLE BROWSER NOTIFICATIONS")

        # ================== HELPERS (esperar visibilidad) ==================
        
        




    def _wait_visible(self, locator: Locator, timeout: int = 10000):
        """Espera a que el locator sea visible."""
        expect(locator).to_be_visible(timeout=timeout)

    def _click_when_visible(self, locator: Locator, timeout: int = 10000):
        """Espera a que sea visible y hace click."""
        self._wait_visible(locator, timeout)
        locator.click()

    # =========================== FLUJOS ================================

    def open(self):
        """Abre la página Your Feed y maneja el modal si aparece."""
        self.page.goto(FEED_URL)
        self._wait_visible(self.title, timeout=10000)
        # Asegúrate de que haya al menos una tarjeta cargada antes de seguir
        expect(self.card).to_be_attached(timeout=10000)
        self.handle_notification_modal()

    def handle_notification_modal(self):
        """Cierra el modal de notificaciones si aparece (espera inteligente)."""
        try:
            self.modal_title.wait_for(state="visible", timeout=8000)  # solo si aparece
            print("🔔 Modal detectado, intentando cerrarlo...")

            if self.maybe_later_btn.is_visible():
                self._click_when_visible(self.maybe_later_btn)
                print("🔕 Modal cerrado con 'MAYBE LATER'.")
            elif self.enable_btn.is_visible():
                self._click_when_visible(self.enable_btn)
                print("🔔 Modal cerrado con 'ENABLE BROWSER NOTIFICATIONS'.")
            else:
                self._click_when_visible(self.modal_dialog.locator("button").first)
                print("⚠️ Modal cerrado mediante clic genérico.")

            expect(self.modal_dialog).to_be_hidden(timeout=5000)
        except PlaywrightTimeoutError:
            print("✅ No apareció el modal de notificaciones.")
        except Exception as e:
            print(f"⚠️ Error al manejar el modal: {e}")

    # ======================= ACCIONES (todas con espera visible) =======================

    def play_from_card(self):
        """Hace click en la tarjeta/botón y verifica que el mini-player quede en estado 'Pause'."""
        boton = self.self.card_play_btn

        # Click para iniciar reproducción hasta que sea visible el boton
        self._click_when_visible(boton)

        # Asegura que el mini-player aparece
        self._wait_visible(self.mini_player, timeout=10000)

        # Espera a que el estado cambie a 'Pause' (está reproduciendo).
        try:
            self._wait_visible(self.mini_pause_btn, timeout=5000)
        except Exception:
        # Si por timing el primer click dejó en 'Play' (o ya estaba playing y lo pausó),
        # intentamos una vez más para forzar 'Pause'.
            self._click_when_visible(boton)
            self._wait_visible(self.mini_player, timeout=8000)
            self._wait_visible(self.mini_pause_btn, timeout=5000)
    def click_repost(self):
        self.handle_notification_modal()
        self._click_when_visible(self.repost_button)
        expect(self.repost_button).to_have_attribute("aria-pressed", "true")

    def open_more_options(self):
        self.handle_notification_modal()
        self._click_when_visible(self.more_options_button)
        self._wait_visible(self.add_playlist_option)

    def create_playlist(self):
        self.handle_notification_modal()
        self._click_when_visible(self.add_playlist_option)
        self._click_when_visible(self.new_playlist_option)
        self._wait_visible(self.confirm_toast, timeout=8000)

    def click_favorite(self):
        self.handle_notification_modal()
        self._click_when_visible(self.favorite_button)
        expect(self.favorite_button).to_have_attribute("aria-pressed", "true")

    def click_share(self):
        self.handle_notification_modal()
        self._click_when_visible(self.share_option)
        self._wait_visible(self.direct_message_option)

    def click_direct_message(self):
        self.handle_notification_modal()
        self._click_when_visible(self.direct_message_option)
        self._wait_visible(self.search_dm, timeout=8000)

    def click_embed(self):
        self.handle_notification_modal()
        self._click_when_visible(self.embedded_option)
        self._wait_visible(self.embed_modal, timeout=8000)

    def click_copy_link(self):
        self.handle_notification_modal()
        self._click_when_visible(self.copy_link_option)
        self._wait_visible(self.confirm_toast, timeout=8000)
