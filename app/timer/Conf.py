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
        }

    ]
