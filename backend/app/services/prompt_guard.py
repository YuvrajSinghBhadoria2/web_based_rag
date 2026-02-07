from typing import List, Optional


class PromptGuardService:
    def __init__(self):
        self.jailbreak_patterns = [
            "ignore previous instructions",
            "disregard all prior",
            "forget everything above",
            "you are now",
            "new role",
            "system:",
            "admin mode",
        ]

        self.restricted_topics = []

    async def validate_input(
        self, query: str, restrictions: Optional[List[str]] = None
    ) -> bool:
        query_lower = query.lower()

        for pattern in self.jailbreak_patterns:
            if pattern in query_lower:
                raise Exception(f"Detected potential jailbreak attempt: '{pattern}'")

        if restrictions:
            for restriction in restrictions:
                if restriction.lower() in query_lower:
                    raise Exception(f"Query violates restriction: '{restriction}'")

        if len(query) > 1000:
            raise Exception("Query exceeds maximum length")

        return True

    async def sanitize_output(self, answer: str) -> str:
        sanitized = answer.strip()

        prefixes_to_remove = ["System:", "Admin:", "Debug:"]
        for prefix in prefixes_to_remove:
            if sanitized.startswith(prefix):
                sanitized = sanitized[len(prefix) :].strip()

        return sanitized

    def set_restrictions(self, topics: List[str]):
        self.restricted_topics = topics


prompt_guard = PromptGuardService()
