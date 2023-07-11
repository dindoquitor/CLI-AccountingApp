class InvalidAttemptChecker:
    def __init__(self, max_attempts):
        self.max_attempts = max_attempts
        self.invalid_attempts = 0

    def increment_attempts(self):
        self.invalid_attempts += 1

    def reset_attempts(self):
        self.invalid_attempts = 0

    def is_max_attempts_exceeded(self):
        return self.invalid_attempts >= self.max_attempts
