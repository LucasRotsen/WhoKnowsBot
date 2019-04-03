from configuration.bot_config import amount_of_terms_to_retrieve
from utils import text_utility, time_utility, twitter_utility
from utils.log_utility import log_info


def how_many_knows(api, term, user_id, user_name):
    log_info("Iniciando análise | QuantosSabem | Usuário: {user} | Termo: {term}".format(user=user_name, term=term),
             "How_Many_Knows")

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
    data["friends_with_knowledge"] = friends_with_knowledge
    data["total_of_specialization"] = total_of_specialization
    data["proportion_of_knowledge"] = proportion_of_knowledge
    data["level_of_specialization"] = level_of_specialization

    log_info(data, "How_Many_Knows")
    log_info("Análise concluída.\n", "How_Many_Knows")

    return data


def who_knows(api, term, user_id, user_name):
    log_info("Iniciando análise | QuemSabe | Usuário: {user} | Termo: {term}".format(user=user_name, term=term),
             "Who_Knows")

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

        suitable_follower_screen_name = twitter_utility.retryable_get_user_name(api, suitable_follower_id)

        data["followers"] = followers
        data["follower_used_term"] = followers_used_term
        data["suitable_follower_score"] = suitable_follower_score
        data["suitable_follower_id"] = suitable_follower_id
        data["suitable_follower_screen_name"] = suitable_follower_screen_name

    log_info(data, "Who_Knows")
    log_info("Análise concluída.\n", "Who_Knows")

    return data


def most_used_terms(api, user_id, user_name):
    log_info("Iniciando análise | SOBREOQUESABEM | Usuário: {user}.".format(user=user_name), "Most_Used_Terms")

    data = {"user_id": user_id, "user_name": user_name}

    friends = twitter_utility.get_user_base(api, user_id, "friends")
    friends_posts = twitter_utility.get_users_posts(api, friends)

    tweets_en = []
    tweets_pt = []

    for friend in friends_posts:
        posts = friends_posts[friend]

        for post in posts:
            tweet = post.text
            culture = post.lang

            if culture == 'pt':
                tweets_pt.append(tweet)

            elif culture == 'en':
                tweets_en.append(tweet)

    words_pt = text_utility.get_filtered_words('portuguese', tweets_pt)
    words_en = text_utility.get_filtered_words('english', tweets_en)

    words = words_pt + words_en
    word_frequency = text_utility.get_word_frequency(words)

    sorted_words_by_frequency = sorted(((value, key) for (key, value) in word_frequency.items()), reverse=True)
    trimmed_sorted_words_by_frequency = sorted_words_by_frequency[:amount_of_terms_to_retrieve]

    # swap keys with values and turn into a dictionary.
    word_frequency_dict = dict((word[1], word[0]) for word in trimmed_sorted_words_by_frequency)

    data["word_frequency"] = word_frequency_dict

    log_info("Análise finalizada | SOBREOQUESABEM | Usuário: {user}.".format(user=user_name), "Most_Used_Terms")

    return data


def get_users_who_used_term(users):
    users_who_used_term = {}

    for user in users:
        if len(users[user][0]) > 0:
            users_who_used_term[user] = users[user][0]

    return users_who_used_term
