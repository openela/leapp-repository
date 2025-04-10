from leapp.models import Model, fields
from leapp.topics import SystemFactsTopic


class SystemFIPSStatus(Model):
    """
    The model represents information about the fips status on OpenELA systems

    """

    topic = SystemFactsTopic

    """
    This field is either enabled or disabled

    """

    fips_status = fields.String()

