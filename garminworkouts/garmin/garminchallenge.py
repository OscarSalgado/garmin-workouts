
import logging
from datetime import datetime

from garminworkouts.garmin.garminwellness import GarminWellness

logger = logging.getLogger(__name__)


class GarminChallenge(GarminWellness):
    _BADGE_CHALLENGE_ENDPOINT = "/badgechallenge-service"

    def list_challenge(self) -> None:
        url: str = f"{self._BADGE_CHALLENGE_ENDPOINT}/badgeChallenge/available"
        challenges: dict = self.get(url).json()
        if challenges == []:
            logger.info("No new available challenges")
        else:
            for challenge in challenges:
                logger.info("Challenge sign up: '%s'", challenge.get("badgeChallengeName"))
                url: str = (
                    f"{self._BADGE_CHALLENGE_ENDPOINT}/badgeChallenge/"
                    f"{challenge.get('uuid')}/optIn/"
                    f"{datetime.today().strftime('%Y-%m-%d')}"
                    )

                self.post(url)
