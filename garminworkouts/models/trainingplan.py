class TrainingPlan(object):
    _TRAININGPLAN_ID_FIELD = 'id'
    _TRAININGPLAN_TYPE_FIELD = 'type'
    _TRAININGPLAN_LEVEL_FIELD = 'level'
    _TRAININGPLAN_VERSION_FIELD = 'version'
    _TRAININGPLAN_NAME_FIELD = 'name'

    @staticmethod
    def extract_trainingplan_id(tp) -> str:
        return tp[TrainingPlan._TRAININGPLAN_ID_FIELD]

    @staticmethod
    def extract_trainingplan_type(tp) -> str:
        return tp[TrainingPlan._TRAININGPLAN_TYPE_FIELD]

    @staticmethod
    def extract_trainingplan_level(tp) -> str:
        return tp[TrainingPlan._TRAININGPLAN_LEVEL_FIELD]

    @staticmethod
    def extract_trainingplan_version(tp) -> str:
        return tp[TrainingPlan._TRAININGPLAN_VERSION_FIELD]

    @staticmethod
    def extract_trainingplan_name(tp) -> str:
        return tp[TrainingPlan._TRAININGPLAN_NAME_FIELD]

    @staticmethod
    def print_trainingplan_summary(tp) -> None:
        tp_ = TrainingPlan.export_trainingplan(tp)
        print("{id} {name:15} {type} {level} {version}".format(**tp_))

    @staticmethod
    def export_trainingplan(tp) -> dict:
        return {
            'id': tp['trainingPlanId'],
            'type': tp['trainingType']['typeKey'],
            'subtype': tp['trainingSubType']['subTypeKey'],
            'level': tp['trainingLevel']['levelKey'],
            'version': tp['trainingVersion']['versionName'],
            'name': tp['name'],
            'description': tp['description'],
            'durationInWeeks': tp['durationInWeeks'],
            'avgWeeklyWorkouts': tp['avgWeeklyWorkouts']
        }
