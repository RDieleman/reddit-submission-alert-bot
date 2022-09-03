# Reddit Submission Alert Bot

Lets you configure a bot account to listen to specific subreddits for posts that match your set filters, and notify you
when new submissions match.

## Configuration

The bot can be configured in the .env file.

### Bot Account

<p>
The bot using the scripts can be registered in your <a href="https://www.reddit.com/prefs/apps/">reddit account preferences</a>. The steps to do so are described <a href="https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps">here</a>.

| Key                                                                   | Explanation                                             |
|:-----------------------------|:--------------------------------------------------------|
| APP_NAME                      | Name of the created app, not the account.               |
| CLIENT_ID             |                                                         |
| CLIENT_SECRET            |                                                         |
| DEVELOPER_USERNAME                     | Username of the developer account connected to the bot. |
| DEVELOPER_PASSWORD | Password of the developer account connected to the bot. |

### Alerts

| Key                                                                   | Explanation                                          |
|:-----------------------------|:-----------------------------------------------------|
| NOTIFY_USERS_LIST                     | Comma separated list of usernames to notify.         |

### Filters

Configure which new submissions you will be notified off.

| Key                   | Explanation                                                                                                                       |
|:----------------------|:----------------------------------------------------------------------------------------------------------------------------------|
| SUBREDDIT_WHITE_LIST  | Comma separated list of subreddit names to listen to for new submissions. Defaults to all.                                        |
| SUBREDDIT_BLACK_LIST  | Comma separated list of subreddit names to ignore when listening to all.                                                          |
| SUBMISSION_WHITE_LIST | Comma separated list of substrings that the submission needs to include in order to be notified. If empty, everything is allowed. |
| SUBMISSION_BLACK_LIST | Comma separated list of substrings that the submission needs to include in order to be ignored. If empty, nothing is blocked.     |
| USER_BLOCK_LIST       | Comma separated list of usernames to ignore.                                                                                      |
