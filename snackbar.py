from kivymd.uix.snackbar import Snackbar


def alert_window(text, zone):
    snackbar_text = ""
    if "momentinis" not in text:
        snackbar_text = f"[color=#000000]{text} Zona: {zone}[/color]"
    else:
        snackbar_text = f"[color=#000000]{text}[/color]"
    Snackbar(
        text=snackbar_text,
        bg_color=(1, 1, 1, 0.8),
        snackbar_x="10dp",
        snackbar_y="10dp",
        pos_hint={"center_x": 0.5},
        size_hint_x=.5,
        duration=7
    ).open()
