import json
import logging

import praw

# Create and configure logger.
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(
    filename='error.log',
    level=logging.ERROR,
    format=LOG_FORMAT,
    filemode='w')
logger = logging.getLogger()

# Load configuration.
with open("config.json", "r") as file:
    config = json.load(file)

# Create Reddit instance.
client = config.get('client')
reddit = praw.Reddit(client_id=client.get('id'),
                     client_secret=client.get('secret'),
                     user_agent='script:{appname} (by u/{username})'.format(
                         appname=client.get('appName'),
                         username=client.get('username')
                     ),
                     username=client.get('username'),
                     password=client.get('password'))

logger.info('Reddit instance started.')


def format_message(submission):
    return '[{title}]({url})\n\nr/{subreddit}'.format(
        subreddit=submission.subreddit,
        title=submission.title,
        url=submission.permalink
    )


def notify_users(subject, message):
    logger.info(message)

    logger.info('Notifying users...')
    for name in config.get('notifiedUsers'):
        reddit.redditor(name).message(subject=subject, message=message)


def get_subreddits():
    subreddit_config = config.get('subreddits')

    # Create a list of subreddits that will be listened to.
    subreddit_filter = 'all'
    subreddit_white_list = "+".join(subreddit_config.get('whitelist'))
    subreddit_black_list = "-".join(subreddit_config.get('blacklist'))

    # If a whitelist exists, overwrite the default 'all' value.
    if len(subreddit_white_list) > 0:
        subreddit_filter = subreddit_white_list

    # Remove blacklisted subreddits from list.
    if len(subreddit_black_list) < 0:
        subreddit_filter = subreddit_filter + "-" + subreddit_black_list

    return reddit.subreddit(subreddit_filter)


def list_item_in_value(l, value, case_sensitive):
    formatted_value = value if case_sensitive else value.lower()

    for item in l:
        formatted_item = item if case_sensitive else item.lower()
        if formatted_item in formatted_value:
            return True

    return False


def should_filter_value(f, value):
    case_sensitive = f.get('caseSensitive')

    overwrite = f.get('overwrite')
    in_overwrite = False if not overwrite else list_item_in_value(overwrite, value, case_sensitive)

    if in_overwrite:
        return False

    whitelist = f.get('whitelist')
    blacklist = f.get('blacklist')

    in_whitelist = True if not whitelist else list_item_in_value(whitelist, value, case_sensitive)
    in_blacklist = False if not blacklist else list_item_in_value(blacklist, value, case_sensitive)

    return not in_whitelist or in_blacklist


def should_filter_submission(submission):
    submission_config = config.get('submissions')
    filters = submission_config.get('filters')

    if not submission.author or submission.author.name in config.get('blockedAuthors'):
        return True

    if not submission_config.get('allowNsfw') and submission.over_18:
        return True

    for f in filters:
        for scope in f.get('scopes'):
            value = ''
            if scope == 'flair':
                value = submission.link_flair_text
                if not value:
                    continue

            elif scope == 'title':
                value = submission.title
            elif scope == 'content':
                value = submission.selftext

            if should_filter_value(f, value):
                return True

    return False


def main():
    logger.info('Started listening for new submissions...')
    for submission in get_subreddits().stream.submissions():
        if should_filter_submission(submission):
            logger.debug('Blocked: https://reddit.com' + submission.permalink)
            continue

        try:
            logger.debug('Notified: https://reddit.com' + submission.permalink)
            notify_users('New Post', format_message(submission))
        except Exception as ex:
            logging.error(ex)


if __name__ == "__main__":
    main()
