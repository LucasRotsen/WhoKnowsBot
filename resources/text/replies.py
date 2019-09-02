def get_positive_how_many_reply(knowledge_str, specialization_str, term, user):
    return "@{user}, {knowledge}% das pessoas que você segue falam sobre {term}. " \
           "O nível de especialização da sua rede a respeito desse assunto é {specialization} em uma escala " \
           "entre 0 e 1." \
        .format(user=user, knowledge=knowledge_str, term=term, specialization=specialization_str)


def get_negative_how_many_reply(term, user):
    return "@{user}, próximo a zero, não encontrei pessoas que você segue falando sobre {term}." \
        .format(user=user, term=term)


def get_positive_who_knows_reply(suitable_follower, term, user):
    return "@{user}, dos seus seguidores quem mais sabe sobre o assunto {term} é @{name}." \
        .format(user=user, term=term, name=suitable_follower)


def get_negative_who_knows_reply(term, user):
    return "@{user}, quase ninguém, seus seguidores não publicam muito sobre {term} " \
        .format(user=user, term=term)


def get_most_used_terms_reply(user):
    return "@{user}, os termos que mais aparecem no seu feed se apresentam na imagem a seguir:" \
        .format(user=user)


def get_invalid_tweet_reply(user):
    return "@{user}, lamento mas não entendi o que você quis dizer." \
        .format(user=user)
