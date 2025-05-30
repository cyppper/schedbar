import rumps
import datetime
import json


def load_schedule():
    with open("schedule.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return [(datetime.datetime.strptime(t, "%H:%M").time(), label) for t, label in data]


class DailyTrayApp(rumps.App):
    def __init__(self):
        super().__init__("", icon=None, menu=[])
        self.schedule = load_schedule()
        self.last_index = None
        self.timer = rumps.Timer(self.refresh_status, 60)
        self.timer.start()
        self.refresh_status(None)

    def refresh_status(self, _):
        now = datetime.datetime.now().time()
        current_index = 0
        current_task = "🕒"
        current_time = now.strftime('%H:%M')

        for i in range(len(self.schedule)):
            start_time, task = self.schedule[i]
            end_time = self.schedule[i + 1][0] if i + 1 < len(self.schedule) else datetime.time(23, 59)
            if start_time <= now < end_time:
                current_index = i
                current_task = self.extract_emoji(task)
                current_time = start_time.strftime('%H:%M')
                current_label = task
                break

        if self.last_index is None:
            self.last_index = current_index
        elif current_index != self.last_index:
            notif_title = f"Новая задача"
            notif_message = f"{current_time} — {current_label}"
            rumps.notification(None, notif_title, notif_message)
            self.last_index = current_index

        self.title = current_task
        self.menu.clear()

        header = rumps.MenuItem("📅 Расписание на день:", callback=lambda _: None)
        header._menuitem.setEnabled_(False)
        self.menu.add(header)

        def dummy_callback(_):
            pass

        for i, (t, task) in enumerate(self.schedule):
            line = f"{t.strftime('%H:%M')} — {task}"
            if i == current_index:
                line = f"👉 {line}"
            item = rumps.MenuItem(line, callback=dummy_callback)
            item._menuitem.setEnabled_(False)
            self.menu.add(item)

    def extract_emoji(self, text):
        return text.split()[0] if text else "❔"


if __name__ == "__main__":
    DailyTrayApp().run()
