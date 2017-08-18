class AlreadyInvitedException(Exception):
    def __init__(self, user):
        super().__init__("{} is already invited to friends list".format(user.__str__()))
