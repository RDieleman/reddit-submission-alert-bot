# Reddit Submission Alert Bot

Lets you configure a bot account to listen to specific subreddits for new submissions that match your set filters, and
notify you
when found.

## Usage

<ol>
<li>Create a config.json file. You can simply rename the existing template.</li>
<li>Register a new bot, described <a href="#client">here</a>.</li>
<li>Using these new credentials, update the client in the config file.</li>
<li>Update the filters in the configuration file to fit your use case.</li>
<li>Install <a href="https://www.docker.com/">Docker</a>.</li>
<li>Using the existing Dockerfile, build a <a href="https://docs.docker.com/engine/reference/commandline/build/">new image</a>.</li>
<li>Using this new image, <a href="https://docs.docker.com/engine/reference/commandline/run/">run the container</a>.</li>
</ol>

## Configuration

The bot can be configured in the config.json file:

### Client

The bot using the scripts can be registered in your <a href="https://www.reddit.com/prefs/apps/">reddit account
preferences</a>. The steps to do so are
described <a href="https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps">here</a>.

| Key      | Explanation                                             |
|:---------|:--------------------------------------------------------|
| appName  | Name of the created app, not the account.               |
| id       |                                                         |
| secret   |                                                         |
| username | Username of the developer account connected to the bot. |
| password | Password of the developer account connected to the bot. |

### Alerts

Users are notified through a reddit message. The user notified can be the same as the developer account, but if you want
to get notifications from the reddit app the account needs to be different.

| Key           | Explanation                  |
|:--------------|:-----------------------------|
| notifiedUsers | List of usernames to notify. |

### Filters

Configure which new submissions you will be notified off.

#### Authors

| Key                          | Explanation                                                |
|:-----------------------------|:-----------------------------------------------------------|
| blockedAuthors               | List of usernames for authors to ignore submissions from.  | 

#### Subreddits

| Key       | Explanation                                                                       |
|:----------|:----------------------------------------------------------------------------------|
| whitelist | List of subreddit names which will be listened to for new posts. Defaults to all. |
| blacklist | List of subreddit names which will be ignored if listening to all.                |

#### Submissions

| Key       | Explanation                                       |
|:----------|:--------------------------------------------------|
| allowNsfw | Set if 18+ posts are included. Defaults to false. |

##### Filters

List of custom filters which are, in order of the configuration, iterated over to determine if a submission should be
ignored or trigger an alert.

| Key           | Explanation                                                                                                                                                         |
|:--------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| scopes        | List of scopes that the filter applies to, consisting of `flair`, `title`, and `content`. Will be iterated over in order of the configuration.                      |
| whitelist     | List of possible substrings that the scope value can include for it to not be filtered out. Defaults to allowing everything.                                        |
| blacklist     | List of possible substrings that the scope value can include for it to be filtered out. Defaults to not blocking anything. Prioritized over being whitelisted.      |
| overwrite     | List of possible substrings that the scope value can include for it to not be filtered out, ignoring the fact if they should depending on the black- and whitelist. |
| caseSensitive | Set if scope values being checked to include substrings should use case sensitivity. Defaults to false.                                                             |