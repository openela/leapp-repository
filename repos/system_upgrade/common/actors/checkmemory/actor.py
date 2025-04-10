from leapp.actors import Actor
from leapp.libraries.actor import checkmemory
from leapp.models import MemoryInfo, Report
from leapp.tags import ChecksPhaseTag, IPUWorkflowTag


class CheckMemory(Actor):
    """
    The actor check the size of RAM against OpenELA8 minimal hardware requirements

    Using the following resource: https://github.com/openela/
    """

    name = 'checkmemory'
    consumes = (MemoryInfo,)
    produces = (Report,)
    tags = (ChecksPhaseTag, IPUWorkflowTag)

    def process(self):
        checkmemory.process()
