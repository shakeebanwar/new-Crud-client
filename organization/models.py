from django.db import models

class Organization(models.Model):
    '''
    Model to store information about the organization
    TODO generally we could add more required information to a organization such as internet site, #employees etc.
    '''
    organization_name               = models.CharField(max_length=60, unique=True)
    creator_user_id                 = models.IntegerField()
    organization_invite_link_append = models.CharField(max_length=64)

    def __str__(self):
        return self.organization_name


class Office(models.Model):
    '''
    Model to store information about offices of organizations
    '''
    office_name         = models.CharField(max_length=50)
    # TODO change location later to Google Maps thingy
    office_location     = models.CharField(max_length=50)
    office_capacity     = models.IntegerField()
    utilization         = models.IntegerField(default=0)
    # 1 Office has 1 Organization, but 1 Organization has many offices
    organization        = models.ForeignKey(Organization, on_delete=models.CASCADE)






