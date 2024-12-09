from data_generation.chatbot_data_generate import generate_from_web_urls


def test_chatbot_app():
    generate_from_web_urls(
        'https://www.aspiresys.com/newsroom/awards-and-recognition/aspire-systems-ceo-gowri-shankar-subramanian-among'
        '-indias-most',
        4)
