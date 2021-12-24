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

    @staticmethod
    def report_user(first_user_name: str, second_user_name: str):
        return f"{first_user_name} has reported {second_user_name}."
    
    @staticmethod
    def want_promotion(user_name: str):
        return f"{user_name} wants to be a host."
