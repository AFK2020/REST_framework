from enum import Enum


class RoleChoice(Enum):
    MANAGER = 'manager'
    QA = 'qa'
    DEVELOPER = 'developer'
    SYSTEM_ARCHITECT = 'system architect'
    NETWORKS_ENGINEER = 'networks engineer'

    @classmethod
    def choices(cls):
        return [(key.value , key.name) for key in cls]


class StatusChoice(Enum):
    OPEN = 'open'
    REVIEW = 'review'
    WORKING = 'working'
    AWAITINGREL = 'waiting release'
    WAITINGQA = 'waiting qa'

    @classmethod
    def choices(cls):
        return [(key.value , key.name) for key in cls]
