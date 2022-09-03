import logging
import os

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


def title_contains_filters(title_lower, filters) -> bool:
    # Check if the title contains filtered substrings.
    for f in filters:
        if f.lower() in title_lower:
            return True

    return False


def notify_user(submission):
    subject = 'New submission found!'
    message = '{title}\n\nr/{subreddit}\n\n{url}'.format(
        subreddit=submission.subreddit,
        title=submission.title,
        url=submission.permalink
    )

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
    title_black_list = get_list_from_config('TITLE_BLACK_LIST')
    title_white_list = get_list_from_config('TITLE_WHITE_LIST')
    user_block_list = get_list_from_config('USER_BLOCK_LIST')

    logger.info('Started listening for new submissions...')
    for submission in reddit.subreddit(subreddit_filter).stream.submissions():
        title_lower = submission.title.lower()

        # Filter submission.
        if (
                (len(title_white_list) > 0 and not title_contains_filters(title_lower, title_white_list))
                or (len(title_black_list) > 0 and title_contains_filters(title_lower, title_black_list))
                or submission.author.name in user_block_list
        ):
            continue

        try:
            notify_user(submission)
        except Exception as ex:
            logging.error(ex)


if __name__ == "__main__":
    main()
