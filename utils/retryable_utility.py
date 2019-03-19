import backoff
from requests import RequestException
from twitter import TwitterError

from utils.log_utility import *


# Retryable methods use the 'backoff' dependency to repeat themselves in case of exception.
# For further information, refer to: https://pypi.org/project/backoff/

@backoff.on_exception(backoff.expo, RequestException, jitter=backoff.full_jitter, on_backoff=log_retry)
def retryable_get_user_timeline(api, max_id, user):
    try:
        return api.GetUserTimeline(count=200, user_id=user, max_id=max_id, exclude_replies=False, include_rts=True)

    # When user account is private a 'Not Authorized' exception will occur.
    except TwitterError as e:
        log_info("Impossível recuperar a timeline. O usuário {id} é privado.".format(id=user),
                 "Retry_Get_User_Timeline")
        return []


@backoff.on_exception(backoff.expo, RequestException, jitter=backoff.full_jitter, on_backoff=log_retry)
def retryable_get_user_id(api, user_name):
    try:
        return api.GetUser(screen_name=user_name).id

    except TwitterError as e:
        log_error(e.message, "retry_get_user_id")


@backoff.on_exception(backoff.expo, RequestException, jitter=backoff.full_jitter, on_backoff=log_retry)
def retryable_get_user_name(api, user_id):
    try:
        return api.GetUser(user_id=user_id).screen_name

    except TwitterError as e:
        log_error(e.message, "retry_get_user_name")


@backoff.on_exception(backoff.expo, RequestException, jitter=backoff.full_jitter, on_backoff=log_retry)
def retryable_get_mentions(api, since_id, max_id):
    try:
        return api.GetMentions(since_id=since_id, max_id=max_id, count=200)

    except TwitterError as e:
        log_error(e.message, "retry_get_mentions")


@backoff.on_exception(backoff.expo, RequestException, jitter=backoff.full_jitter, on_backoff=log_retry)
def retryable_get_friend_ids(api, user_id):
    try:
        return api.GetFriendIDs(user_id=user_id)

    except TwitterError as e:
        log_error(e.message, "retry_get_friend_ids")


@backoff.on_exception(backoff.expo, RequestException, jitter=backoff.full_jitter, on_backoff=log_retry)
def retryable_get_follower_ids(api, user_id):
    try:
        return api.GetFollowerIDs(user_id=user_id)

    except TwitterError as e:
        log_error(e.message, "retry_get_follower_ids")


@backoff.on_exception(backoff.expo, RequestException, jitter=backoff.full_jitter, on_backoff=log_retry)
def retryable_post_update(api, status, mention_id, media=None):
    try:
        api.PostUpdate(status=status, in_reply_to_status_id=mention_id, media=media, auto_populate_reply_metadata=True)

    except TwitterError as e:
        log_error(e.message, "retry_post_update")
