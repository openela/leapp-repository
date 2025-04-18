from leapp.models import fields, Model, Module
from leapp.topics import TransactionTopic


class RpmTransactionTasks(Model):
    topic = TransactionTopic

    local_rpms = fields.List(fields.String(), default=[])
    to_install = fields.List(fields.String(), default=[])
    to_keep = fields.List(fields.String(), default=[])
    to_remove = fields.List(fields.String(), default=[])
    to_upgrade = fields.List(fields.String(), default=[])
    to_exclude = fields.List(fields.String(), default=[])
    modules_to_enable = fields.List(fields.Model(Module), default=[])
    modules_to_reset = fields.List(fields.Model(Module), default=[])


class FilteredRpmTransactionTasks(RpmTransactionTasks):
    pass


class PESRpmTransactionTasks(RpmTransactionTasks):
    # Introduced because the framework struggles with solving dependency order of actors:
    # https://github.com/oamg/leapp/issues/491
    pass
