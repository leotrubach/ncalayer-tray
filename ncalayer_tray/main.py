import asyncio
import datetime
import json
import pathlib
import ssl


from datetime import timezone
import websockets

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

SETTINGS_CMD = "showSettings"
MODULES_CMD = "showBundleManager"
MODULE = "kz.gov.pki.ncalayerservices.accessory"


async def send_ws_cmd(cmd):
    ssl_context = ssl._create_unverified_context()
    async with websockets.connect(
        "wss://127.0.0.1:13579/", ssl=ssl_context
    ) as websocket:
        await websocket.send(json.dumps({"module": MODULE, "method": cmd}))
        await websocket.recv()


def open_settings(*args, **kwargs):
    asyncio.run(send_ws_cmd(SETTINGS_CMD))


def open_bundle_manager(*args, **kwargs):
    asyncio.run(send_ws_cmd(MODULES_CMD))


def close_app(*args, **kwargs):
    Gtk.main_quit()


def make_menu(event_button, event_time, data=None):
    menu = Gtk.Menu()
    settings_item = Gtk.MenuItem(label="Settings")
    bundle_manager = Gtk.MenuItem(label="Bundle manager")
    close_item = Gtk.MenuItem(label="Close App")

    # Append the menu items
    menu.append(settings_item)
    menu.append(bundle_manager)
    menu.append(close_item)
    # add callbacks
    settings_item.connect_data("activate", open_settings, "Open App")
    bundle_manager.connect_data("activate", open_bundle_manager, "Open App")
    close_item.connect_data("activate", close_app, "Close App")
    # Show the menu items
    settings_item.show()
    bundle_manager.show()
    close_item.show()

    # Popup the menu
    menu.popup(None, None, None, None, event_button, event_time)


def on_right_click(data, event_button, event_time):
    make_menu(event_button, event_time)


def on_left_click(event_button):
    make_menu(2, int(datetime.datetime.now().timestamp()))


def main():
    icon = Gtk.StatusIcon()
    icon.set_from_icon_name(Gtk.STOCK_ABOUT)
    icon.connect("popup-menu", on_right_click)
    icon.connect("activate", on_left_click)
    Gtk.main()


if __name__ == "__main__":
    main()
