from abc import ABC, abstractmethod


class SecurityAnalyzer(ABC):
    analyzer_name = "Generic Security Analyzer"

    @abstractmethod
    def analyze(self, *args, **kwargs):
        pass
