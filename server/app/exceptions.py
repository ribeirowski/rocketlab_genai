class AgentException(Exception):
    pass

class RateLimitException(Exception):
    pass

class GuardrailException(Exception):
    pass

class UnsafeSQLException(AgentException):
    def __init__(self, sql: str):
        super().__init__(f"Unsafe SQL blocked: {sql[:120]}")
        self.sql = sql
        
class SQLGenerationException(AgentException):
    pass

class DatabaseQueryException(AgentException):
    pass