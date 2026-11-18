
# -*- coding: utf-8 -*-

from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.MenuList import MenuList
from Components.ActionMap import ActionMap
from Components.Label import Label
import shutil
import subprocess


class NovalerAssistant(Screen):

    skin = """
    <screen name="NovalerAssistant"
        position="center,center" size="850,560"
        title="Novaler Assistant">
        <widget name="title" position="20,15"
            size="810,60" font="Regular;30"
            halign="center" />
        <widget name="menu" position="40,100"
            size="770,400" font="Regular;26"
            scrollbarMode="showOnDemand" />
    </screen>
    """

    def __init__(self, session):
        Screen.__init__(self, session)

        self["title"] = Label("مساعد نوفالر")
        self["menu"] = MenuList([
            "معلومات الجهاز",
            "حالة الشبكة",
            "مساحة التخزين",
            "حول التطبيق",
            "خروج"
        ])

        self["actions"] = ActionMap(
            ["OkCancelActions", "DirectionActions"],
            {
                "ok": self.open_item,
                "cancel": self.close,
                "up": self["menu"].up,
                "down": self["menu"].down,
            },
            -1
        )

    def show_message(self, title, message):
        self.session.open(
            MessageBox,
            message,
            type=MessageBox.TYPE_INFO,
            title=title,
            timeout=15
        )

    def open_item(self):
        choice = self["menu"].getCurrent()

        if choice == "معلومات الجهاز":
            try:
                with open("/etc/image-version", "r") as f:
                    info = f.read()
            except Exception:
                info = "تعذر قراءة معلومات النظام"

            self.show_message("معلومات الجهاز", info[:2500])

        elif choice == "حالة الشبكة":
            try:
                result = subprocess.check_output(
                    ["ip", "-4", "-o", "addr", "show",
                     "scope", "global"],
                    stderr=subprocess.DEVNULL,
                    text=True
                )
                message = result if result.strip() else "لا يوجد اتصال شبكة"
            except Exception:
                message = "تعذر قراءة حالة الشبكة"

            self.show_message("حالة الشبكة", message[:1500])

        elif choice == "مساحة التخزين":
            try:
                usage = shutil.disk_usage("/")
                total = usage.total / (1024 ** 3)
                used = usage.used / (1024 ** 3)
                free = usage.free / (1024 ** 3)

                message = (
                    f"الإجمالي: {total:.2f} GB\n"
                    f"المستخدم: {used:.2f} GB\n"
                    f"المتاح: {free:.2f} GB"
                )
            except Exception:
                message = "تعذر قراءة مساحة التخزين"

            self.show_message("مساحة التخزين", message)

        elif choice == "حول التطبيق":
            self.show_message(
                "حول التطبيق",
                "Novaler Assistant\n"
                "الإصدار 1.0.0\n"
                "مساعد عربي لأجهزة Novaler Enigma2"
            )

        elif choice == "خروج":
            self.close()


def main(session, **kwargs):
    session.open(NovalerAssistant)


def Plugins(**kwargs):
    return [
        PluginDescriptor(
            name="Novaler Assistant",
            description="مساعد عربي لجهاز Novaler",
            where=PluginDescriptor.WHERE_PLUGINMENU,
            fnc=main
        )
    ]

