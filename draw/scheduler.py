import random
from django.utils import timezone
from draw.models import DrawManager, DrawApplicant
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.utils.timezone import now


def start_scheduler():
    scheduler = BackgroundScheduler()

    # 매 1분마다 draw_winner 실행
    scheduler.add_job(
        draw_winner,
        trigger=CronTrigger(minute="*"),  # 1분마다 실행
        id="draw_winner_job",  # 유니크 ID (중복 방지)
        replace_existing=True,  # 기존 작업 교체
    )

    # 스케줄러 시작
    scheduler.start()
    print(f"Scheduler started at {now()}")


def draw_winner():
    draw_managers = DrawManager.objects.filter(state=0, crontab=True, draw_time__lt=timezone.now())

    if not draw_managers:
        print("No draw manager found with state=0, crontab=True and valid draw_time.")
        return

    for draw_manager in draw_managers:
        print(f"Processing draw manager {draw_manager.uuid}...")

        applicants = DrawApplicant.objects.filter(draw_uuid=draw_manager.uuid, is_winner=False)

        if len(applicants) < draw_manager.draw_num:
            print(f"Not enough applicants to draw for draw manager {draw_manager.uuid}.")
            continue

        winners = random.sample(list(applicants), draw_manager.draw_num)

        for winner in winners:
            winner.is_winner = True
            winner.save()

        draw_manager.state = 1
        draw_manager.save()

        print(f"{draw_manager.draw_num} winners have been selected for draw manager {draw_manager.uuid}.")
    return