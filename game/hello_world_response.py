from dataclasses import dataclass


@dataclass
class HelloWorldResponse:
    good: bool

    def serialize(self) -> dict[str, object]:
        return {"good": self.good}
