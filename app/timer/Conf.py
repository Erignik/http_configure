class TimerConfig(object):
    JOBS = [
        {
            'id': 'job1',
            'func': 'timer.CheckDefaultValue:check_default_value',
            'trigger': 'interval',
            'seconds': 1800
        },
        {
            'id': 'job2',
            'func': 'timer.BackupDbFile:backup_db_file',
            'trigger': 'interval',
            'seconds': 3600
        },
        {
            'id': 'job3',
            'func': 'timer.OneSecTrigger:one_sec_trigger',
            'trigger': 'interval',
            'seconds': 1
        },
        {
            'id': 'job4',
            'func': 'timer.OneMinTrigger:one_min_trigger',
            'trigger': 'interval',
            'seconds': 60
        }

    ]
