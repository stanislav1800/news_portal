from apscheduler.schedulers.background import BackgroundScheduler

appointment_scheduler = BackgroundScheduler()
appointment_scheduler.add_job(
    id='send mails', func=lambda :print(), trigger='interval', seconds=5
)

