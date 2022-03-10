#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# encoding: utf8
"""
Simple job scheduler

Todo:
- Add the possibility to exec job at specific times (eg. first of
month, every Monday at 00:01, etc...)
- Make tasks accept a list of jobs to run
"""
# pylint: disable=too-many-arguments, line-too-long
import time
from typing import Callable, Final
from uuid import uuid4


class Job:
    """Job"""

    def __init__(self, job: Callable, tag: str=None) -> None:
        self._job = job
        self._tags = [] if not tag else [tag]
        self._last_exec = time.time()

    def add_tag(self, tag: str) -> None:
        """
        Sets the job's tag

        Raises: ValueError if this tag is already associated with this job
        """
        if tag in self._tags:
            raise ValueError(f'The tag {tag} is already associated to this job')
        self._tags.append(tag)

    def remove_tag(self, tag: str) -> None:
        """
        Removes one tag from the job's tags

        Raises: ValueError if there is no such tag associated with this job
        """
        self._tags.remove(tag)

    def run(self) -> None:
        """Run the job"""
        self._job()
        self._last_exec = time.time()

    @property
    def last_exec(self) -> float:
        """epoch timestamp from this job's last execution"""
        return self._last_exec


class TaskScheduler:
    """Task Scheduler"""

    SECOND: Final = 1
    MINUTE: Final = SECOND * 60
    HOUR: Final = MINUTE * 60

    def __init__(self) -> None:
        self.jobs = {}

    def set_interval_task(self, job: Callable, seconds: int=0, minutes: int=0, hours: int=0, tag=None) -> str:
        """
        Creates a new task by adding a job to the scheduler. This job
        will then be executed periodically

        Args:
            (Callable)  job:        the job function to execute
            (int)       seconds:    the number of seconds to wait for
            (int)       minutes:    the number of mminutes to wait for
            (int)       hours:      the number of hours to wait for
            (str)       tag:        an optional tag for easy retrieve

        Returns:
            (str) unique id associated to the task created

        Raises:
            RuntimeError: missing a time unit
        """
        if seconds == 0 and minutes == 0 and hours == 0:
            raise RuntimeError('At least one time unit must be set')

        interval = seconds + minutes * self.MINUTE + hours * self.HOUR
        task_id = str(uuid4())

        self.jobs.update({task_id: {'job': Job(job, tag), 'interval': interval}})

        return task_id

    # def set_interval_at(self, ):
    #     pass

    def poll(self) -> None:
        """Executing this at regular interval will trigger job that needs to run"""
        now = time.time()
        for task_id, task in self.jobs.items():
            job = task.get('job')
            if now >= job.last_exec + task.get('interval'):
                print(f'Running {task_id}: {task}')
                job.run()
