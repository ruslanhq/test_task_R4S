from django.core.exceptions import ValidationError
from .models import Robot


def process_data(data: dict) -> Robot:
    """
    Processes and validates input data before saving it in the database.

    Args:
        data (dict): Input data in JSON format.

    Returns:
        robot (Robot): Saved instance of Robot model.
    """
    try:
        robot = Robot.objects.create(
            model=data['model'],
            version=data['version'],
            created=data['created']
        )
    except KeyError:
        raise ValidationError('Invalid input data. Missing required fields.')

    robot.save()
    return robot
