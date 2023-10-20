# ☻ importing my model from courses/models/course/Course
# ↓ makes it possible to be registered in admin panel
# ↑ this import creates a sharper directory paths
from apps.courses.models.course import Course,Learning,Prerequisite,Tag
from apps.courses.models.video import Video