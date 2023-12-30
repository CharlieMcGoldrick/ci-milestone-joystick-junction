from django.apps import AppConfig


class MessageBoardConfig(AppConfig):
    """
    MessageBoardConfig is the application configuration for the message_board
    application. It includes settings for the application such as the default
    auto field and the name.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'message_board'