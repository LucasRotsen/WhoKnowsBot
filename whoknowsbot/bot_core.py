from configuration.bot_config import verbose
from utils import time_utility, twitter_utility


def how_many_knows(api, term, user_id, user_name):
    if verbose:
        print("Iniciando análise | QUANTOSSABEM")
        print("Usuário: " + str(user_name) + ". Termo: " + term + ".")

    data = {}

    friends_with_knowledge = 0
    total_of_specialization = 0

    friends = twitter_utility.get_user_base(api, user_id, "friends")
    friends_posts = twitter_utility.get_users_posts_term(api, friends, term)
    friends_used_term = get_users_who_used_term(friends_posts)

    for friend in friends_used_term:
        friend_actions_with_term = len(friends_used_term[friend])

        if friend_actions_with_term > 0:
            friends_with_knowledge += 1
            total_of_specialization += friend_actions_with_term / friends_posts[friend][1]

    proportion_of_knowledge = friends_with_knowledge / len(friends)
    level_of_specialization = total_of_specialization / len(friends)

    data["term"] = term
    data["user_id"] = user_id
    data["user_name"] = user_name
    data["friends"] = friends
    data["friends_used_term"] = friends_used_term
    data["friends_with_knowledge"] = friends_with_knowledge
    data["total_of_specialization"] = total_of_specialization
    data["proportion_of_knowledge"] = proportion_of_knowledge
    data["level_of_specialization"] = level_of_specialization

    if verbose:
        print(data)
        print("Análise concluída." + "\n")

    return data


def who_knows(api, term, user_id, user_name):
    if verbose:
        print("Iniciando análise | QUEMSABE")
        print("Usuário: " + str(user_name) + ". Termo: " + term + ".")

    data = {"term": term, "user_id": user_id, "user_name": user_name}

    followers = twitter_utility.get_user_base(api, user_id, "followers")
    followers_post = twitter_utility.get_users_posts_term(api, followers, term)
    followers_used_term = get_users_who_used_term(followers_post)

    lowest_timestamp = twitter_utility.get_oldest_tweet_timestamp(followers_used_term)

    if lowest_timestamp != 9999999999999:
        current_timestamp = time_utility.get_current_timestamp()
        suitable_follower_score = 0
        suitable_follower_id = None

        for follower in followers_used_term:
            score = 0

            for tweet in followers_used_term[follower]:
                if tweet.retweeted_status is not None:
                    score = score + 0.5

                elif tweet.in_reply_to_user_id is not None:
                    score = score + 1.0

                else:
                    score = score + 0.75

                tweet_timestamp = time_utility.convert_to_timestamp(tweet.created_at)
                score = score + (1 - (current_timestamp - tweet_timestamp) / (current_timestamp - lowest_timestamp))

            if score > suitable_follower_score:
                suitable_follower_score = score
                suitable_follower_id = follower

        suitable_follower_screen_name = twitter_utility.get_user_name(api, suitable_follower_id)

        data["followers"] = followers
        data["follower_used_term"] = followers_used_term
        data["suitable_follower_score"] = suitable_follower_score
        data["suitable_follower_id"] = suitable_follower_id
        data["suitable_follower_screen_name"] = suitable_follower_screen_name

    if verbose:
        print(data)
        print("Análise concluída." + "\n")

    return data


def get_users_who_used_term(users):
    users_who_used_term = {}

    for user in users:
        if len(users[user][0]) > 0:
            users_who_used_term[user] = users[user][0]

    return users_who_used_term
