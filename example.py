#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# encoding: utf8
"""
Example of job"""
import sys
import time
from datetime import datetime

from job_scheduler import TaskScheduler


def print_current_time():
    """Example job"""
    sys.stdout.write(f'Current time: {datetime.now()}\n')


def main():
    """Main"""
    pct_job = TaskScheduler()
    pct_job.set_interval_task(print_current_time, seconds=10, tag='pct')

    while True:
        try:
            pct_job.poll()
            time.sleep(1)
        except KeyboardInterrupt:
            print('\nBye!')
            sys.exit(0)


if __name__ == '__main__':
    main()
