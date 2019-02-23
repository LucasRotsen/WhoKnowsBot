from wordcloud import WordCloud


def get_wordcloud(dict):
    wordcloud = WordCloud(width=400, height=400,
                          background_color='white',
                          min_font_size=10).generate_from_frequencies(dict)

    return wordcloud


def save_wordcloud_image(name, path, wordcloud):
    image_path = path + name + ".jpg"
    wordcloud.to_file(image_path)

    return image_path
