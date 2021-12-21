class NotificationMessage():
    @staticmethod
    def approvedPromotion():
        return "Congratulations! You are now a host. You can now create events."
    
    @staticmethod
    def declinedPromotion():
        return "Sorry! Your request for promotion is declined."
    
    @staticmethod
    def ban_user(reason: str):
        return f"You are banned. Reason: {reason}"

    @staticmethod
    def unban_user():
        return "You are unbanned now."