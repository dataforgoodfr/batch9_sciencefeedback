from sandboxes.creators.ci.create_or_modify_researchers import *
from utils.logger import logger


def create_sandbox():
    logger.info('create_ci_sandbox...')
    create_or_modify_researchers()
    logger.info('create_ci_sandbox...Done.')
