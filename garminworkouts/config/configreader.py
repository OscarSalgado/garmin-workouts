import logging
import os
from typing import Any

import yaml

from garminworkouts.config.includeloader import IncludeLoader

logger = logging.getLogger(__name__)


def read_config(filename: str) -> dict[str, Any]:
    with open(filename, 'r') as f:
        data: dict = yaml.load(f, IncludeLoader)
        test_name: str = os.path.basename(filename).split('.')[0]
        s: str = data.get('name', '').split('-')[0].replace(
            'D', '_').replace('W0', 'R').replace('W', 'R').replace(' ', '')

        if 'steps' in data:
            steps = []
            for step in data.get('steps', []):
                if isinstance(step, list) and isinstance(step[0], list):
                    for u in step[0]:
                        if isinstance(u, list):
                            u = u[0]
                            steps.append(u)
                        else:
                            steps.append(u)
                else:
                    steps.append(step)
            data['steps'] = steps
            if isinstance(data['steps'], list) and len(data['steps']) == 1 and isinstance(data['steps'][0], list):
                data['steps'] = data['steps'][0]
            if s not in test_name and 'goal' not in data:
                logger.warning("Name in config file '%s' does not match filename '%s'", s, test_name)
        else:
            if 'content' in data:
                if '-' in data['name']:
                    data['name'] = test_name + '-' + data.get('name', '').split('-')[1]
                else:
                    data['name'] = test_name + '-' + data.get('name', '')
        data['file'] = filename
    return data
