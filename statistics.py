import firebase_conn
from datetime import datetime
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from itertools import count


def get_statistics(anchor, user_id):
    ref = firebase_conn.db.reference("/stats")
    stats = ref.get()
    anchor.clear_widgets()
    i = count(start=1)
    try:
        data_tables = MDDataTable(
            size_hint=(0.9, 0.6),
            use_pagination=True,
            column_data=[
                ("No.", dp(7)),
                ("Matuoklis", dp(20)),
                ("Data", dp(20)),
                ("Laikas", dp(20))
            ],
            row_data=[
                    (f"{next(i)}", value["class"], value["data"], value["time"]) for key, value in stats.items()
                    if value["user_id"] == user_id
            ]
        )
        anchor.add_widget(data_tables)
    except Exception as e:
        print(e)


def post_statistics(cls, user_id):
    ref = firebase_conn.db.reference("/stats")
    current_datetime = datetime.now()
    print("posting")
    try:
        ref.push(
            {
                "user_id": user_id,
                "class": cls,
                "data": datetime.now().date().isoformat(),
                "time": current_datetime.strftime("%H:%M:%S")
            }
        )
    except Exception as e:
        print(e)
