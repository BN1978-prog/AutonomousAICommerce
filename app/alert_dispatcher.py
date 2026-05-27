from app.send_telegram_alert import send_alert

def notify(event_type,payload):

    handlers={

        "SYSTEM_ERROR":
        lambda p: send_alert(
            "SYSTEM ERROR",
            p
        ),

        "NEW_ORDER":
        lambda p: send_alert(
            "NEW ORDER",
            p
        ),

        "LOW_INVENTORY":
        lambda p: send_alert(
            "LOW INVENTORY",
            p
        ),

        "WINNER_PRODUCT":
        lambda p: send_alert(
            "WINNER PRODUCT",
            p
        ),

        "CAMPAIGN_WAITING_APPROVAL":
        lambda p: send_alert(
            "CAMPAIGN READY",
            p
        ),

        "SCALE_CANDIDATE":
        lambda p: send_alert(
            "SCALE CANDIDATE",
            p
        ),

        "CEO_DASHBOARD":
        lambda p: send_alert(
            "CEO DASHBOARD",
            p
        )
    }

    if event_type in handlers:
        handlers[event_type](payload)

if __name__=="__main__":
    notify(
        "WINNER_PRODUCT",
        "pet_brush | score=24"
    )
