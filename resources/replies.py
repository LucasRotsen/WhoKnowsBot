def get_negative_how_many_reply(term, user):
    return "Olá @{user}, infelizmente não encontrei ninguém entre quem você segue " \
           "falando sobre #{term} :(" \
        .format(user=user, term=term)


def get_positive_how_many_reply(knowledge_str, specialization_str, term, user):
    return "Olá @{user}, {knowledge}% das pessoas que você segue falam sobre #{term}. " \
           "O nível de especialização da sua rede é {specialization} em uma escala entre 0 e 1. " \
           "Diga-me, de 1 a 5, o quanto você concorda com esta resposta :)" \
        .format(user=user, knowledge=knowledge_str, term=term, specialization=specialization_str)


def get_positive_who_knows_reply(suitable_follower, term, user):
    return "Olá @{user}, entre seus seguidores quem mais sabe sobre #{term}" \
           " é @{name}. Diga-me, de 1 a 5, o quanto você concorda com esta resposta :)" \
        .format(user=user, term=term, name=suitable_follower)


def get_negative_who_knows_reply(term, user):
    return "Olá @{user}, infelizmente não encontrei ninguém entre seus seguidores que " \
           "sabe sobre #{term} :(" \
        .format(user=user, term=term)


def get_most_used_terms_reply(user):
    return "Olá @{user}, os termos mais usados na sua timeline são:" \
        .format(user=user)


def get_invalid_tweet_reply(user):
    return "É constrangedor @{user}, mas não consegui te entender :(. " \
           "Você pode olhar meus tweets anteriores como exemplo e tentar mais uma vez." \
        .format(user=user)
