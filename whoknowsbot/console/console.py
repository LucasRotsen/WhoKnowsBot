from utils.file_utility import write
from utils.twitter_utility import retryable_get_user_id
from whoknowsbot.core import most_used_terms


def get_user_data_with_term(api, user_name, term):
    user_id = retryable_get_user_id(api, user_name)

    data = {
        # "how_many_knows": how_many_knows(api, term, user_id, user_name),
        # "who_knows": who_knows(api, term, user_id, user_name),
        "most_used_terms": most_used_terms(api, user_id, user_name)
    }

    write("result.txt", str(data))
