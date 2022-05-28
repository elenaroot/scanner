from django.db import models


class State(models.IntegerChoices):
    ACC = 1, "Accepted"
    RUN = 2, "Running"
    ERR = 3, "Error"
    COM = 4, "Complete"
    NOT = 5, "Not-Found"


# Create your models here.
class Scan(models.Model):
    domain = models.CharField(max_length=256, unique=True, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    state = models.PositiveSmallIntegerField(
        choices=State.choices,
        default=State.ACC
    )

    def __str__(self):
        return f"Scan(id=[{self.id}], domain=[{self.domain}], state=[{self.get_state_display()}])"
