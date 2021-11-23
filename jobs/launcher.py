# -*- coding: utf-8 -*-
import time
import sys
import argparse
from flask_script import Command, Option
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler
from jobs import credit
from datetime import datetime, timedelta
from common import Log


class StartScheduler(Command):
    capture_all_args = True
    scheduler = None

    def run(self, *args, **kwargs):
        args = sys.argv[2:]
        parser = argparse.ArgumentParser(add_help=True)
        parser.add_argument("-m", "--name", dest="name", metavar="name", help="指定job名")
        # parser.add_argument("-a", "--act", dest="act", metavar="act", help="Job动作", required=False)
        parser.add_argument("-p", "--param", dest="param", nargs="*", metavar="param", help="业务参数", default='',
                            required=False)
        params = parser.parse_args(args)
        params_dict = params.__dict__
        ret_params = {}
        for item in params_dict.keys():
            ret_params[item] = params_dict[item]

        print('[{}] Start scheduler main processor.'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        if "name" in ret_params and ret_params['name'] is not None:
            try:
                self.scheduler = BlockingScheduler()
                # 执行指定任务
                self.do_single(params=ret_params)
                self.scheduler.start()
            except (KeyboardInterrupt, SystemExit):
                print("Exit scheduler.")
        else:
            job_defaults = {
                            'max_instances': 2,
                            'coalesce': True,
                            }
            self.scheduler = BackgroundScheduler(job_defaults=job_defaults)
            # 执行全部任务
            self.do_all()
            self.scheduler.start()
            while True:
                """
                # 每天凌晨 00:00 关闭 scheduler，通过系统crontab重启
                if datetime.now().hour == 0:
                    print("[{}] Shutdown scheduler main processor.".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                    try:
                        self.scheduler.shutdown()
                    except SchedulerNotRunningError:
                        print("[{}] Scheduler is not running".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                        exit(0)
                """
                print('[{}] Scheduler main processor is running.'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                time.sleep(3600)

    def do_single(self, params):
        # 执行单个任务
        param_args = dict()
        if len(params['param']) > 0:
            for param in params['param'][0].split(','):
                param_args[str(param.split('=')[0])] = str(param.split('=')[1])
        deadline = datetime.now().replace(microsecond=0) + timedelta(seconds=1)
        try:
            self.scheduler.add_job(id='Manual execute job: {}'.format(params['name']),
                                   func=eval(params['name']),
                                   next_run_time=deadline,
                                   trigger='date',
                                   kwargs=param_args
                                   )
        except AttributeError as e:
            Log.warn(e)

    def do_all(self):
        pass
