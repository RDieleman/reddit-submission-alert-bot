import logging
import os
from datetime import datetime

import praw
from dotenv import load_dotenv

# Create and configure logger.
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(
    filename='error.log',
    level=logging.ERROR,
    format=LOG_FORMAT,
    filemode='w')
logger = logging.getLogger()

# Load environment variables from file.
load_dotenv()

# Create Reddit instance.
reddit = praw.Reddit(client_id=os.getenv('CLIENT_ID'),
                     client_secret=os.getenv('CLIENT_SECRET'),
                     user_agent='script:{appname} (by u/{username})'.format(
                         appname=os.getenv('APP_NAME'),
                         username=os.getenv('DEVELOPER_USERNAME')
                     ),
                     username=os.getenv('DEVELOPER_USERNAME'),
                     password=os.getenv('DEVELOPER_PASSWORD'))

logger.info('Reddit instance started.')


def get_list_from_config(key) -> [str]:
    # Lists are comma separated.
    items = os.getenv(key, '').split(',')

    while '' in items:
        items.remove('')

    return items


def submission_contains_filters(submission, filters, contains_all) -> bool:
    # Check if the title or selftext contains filtered substrings.
    for f in filters:
        if f.lower() in submission.title.lower():
            if not contains_all:
                return True

            continue

        if f.lower() in submission.selftext.lower():
            if not contains_all:
                return True

            continue

        if contains_all:
            return False

    if contains_all:
        return True

    return False


def format_message(submission):
    return '[{title}]({url})\n\nr/{subreddit}'.format(
        subreddit=submission.subreddit,
        title=submission.title,
        url=submission.permalink
    )


def notify_users(subject, message):
    logger.info(message)

    logger.info('Notifying users...')
    for name in get_list_from_config('NOTIFY_USERS_LIST'):
        reddit.redditor(name).message(subject=subject, message=message)


def main():
    # Create a list of subreddits that will be listened to.
    subreddit_filter = 'all'
    subreddit_white_list = "+".join(get_list_from_config('SUBREDDIT_WHITE_LIST'))
    subreddit_black_list = "-".join(get_list_from_config('SUBREDDIT_WHITE_LIST'))

    # If a whitelist exists, overwrite the default 'all' value.
    if len(subreddit_white_list) > 0:
        subreddit_filter = subreddit_white_list

    # Remove blacklisted subreddits from list.
    if len(subreddit_black_list) < 0:
        subreddit_filter = subreddit_filter + "-" + subreddit_black_list

    # Create filters for individual submissions.
    submission_black_list = get_list_from_config('SUBMISSION_BLACK_LIST')
    submission_white_list = get_list_from_config('SUBMISSION_WHITE_LIST')
    submission_must_contain_list = get_list_from_config('SUBMISSION_MUST_CONTAIN_LIST')
    user_block_list = get_list_from_config('USER_BLOCK_LIST')

    logger.info('Started listening for new submissions...')
    last_status_notify = datetime.utcnow()
    for submission in reddit.subreddit(subreddit_filter).stream.submissions():
        # Notify user about service health.
        now = datetime.utcnow()
        if 23 < now.hour < 24 and last_status_notify.timestamp() > now.timestamp() + (60 * 60 * 23):
            notify_users('Service online.', '')
            last_status_notify = datetime.utcnow()

        # Filter submission.
        if (
                submission.author is None  # author has deleted their account.
                or (
                len(submission_white_list) > 0 and not submission_contains_filters(submission, submission_white_list,
                                                                                   False))
                or (len(submission_black_list) > 0 and submission_contains_filters(submission, submission_black_list,
                                                                                   False))
                or (len(submission_must_contain_list) > 0 and not submission_contains_filters(submission,
                                                                                              submission_must_contain_list,
                                                                                              True))
                or submission.author.name in user_block_list
        ):
            continue

        try:
            notify_users('Submission found!', format_message(submission))
        except Exception as ex:
            logging.error(ex)


if __name__ == "__main__":
    main()
