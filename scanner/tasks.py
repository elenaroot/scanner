from __future__ import absolute_import, unicode_literals
import logging
import os
import random
from datetime import timedelta
from enum import IntEnum
from celery import shared_task
from scanner.models import Scan, State
from django.utils.timezone import now

logger = logging.getLogger('django')


class ScanResult(IntEnum):
    SUCCESS = 0
    FAILURE = 1


def run_scan(domain):
    response = random.choice([0, 1])  # os.system("ping -c 1 " + domain)
    logger.info(f"run_scan: scanning domain=[{domain}], response=[{response}].")
    return ScanResult.SUCCESS if response == 0 else ScanResult.FAILURE


@shared_task
def process_scan(scan_id):
    logger.info(f"process_scan: called with scan_id=[{scan_id}].")
    scan = Scan.objects.get(id=scan_id)
    scan.state = State.RUN
    scan.save()
    res = run_scan(scan.domain)
    scan.state = State.COM if res == ScanResult.SUCCESS else State.ERR
    scan.save()
    logger.info(f"process_scan: finished for scan_id=[{scan_id}].")


@shared_task
def cleanup_task():
    logger.info(f"cleanup_task: started .")
    cnt, _ = Scan.objects.filter(updated__lt=now() - timedelta(minutes=20)).delete()
    logger.info(f"cleanup_task: finished, deleted cnt=[{cnt}] .")
