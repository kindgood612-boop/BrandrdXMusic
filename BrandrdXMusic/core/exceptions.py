class AssistantErr(Exception):
    """
    Exception خاصة بالـ Assistant (PyTgCalls / Music Player)
    """
    def __init__(self, message: str = "Assistant Error"):
        super().__init__(message)
