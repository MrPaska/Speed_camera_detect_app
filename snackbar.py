from kivymd.uix.snackbar import Snackbar


def alert_window(text, zone):
    Snackbar(
        text=f"[color=#000000]{text} Zona: {zone}[/color]",
        bg_color=(1, 1, 1, 0.8),
        snackbar_x="10dp",
        snackbar_y="10dp",
        pos_hint={"center_x": 0.5},
        size_hint_x=.5,
        duration=7
    ).open()

