class TimerConfig(object):
    JOBS = [
        {
            'id': 'job1',
            'func': 'timer.CheckDefaultValue:check',
            'args': (1, 2),
            'trigger': 'interval',
            'seconds': 5
        }
    ]
