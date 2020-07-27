class TimerConfig(object):
    JOBS = [
        {
            'id': 'job1',
            'func': 'timer.CheckDefaultValue:check_default_value',
            'trigger': 'interval',
            'seconds': 3600
        }
    ]
