# blue prints are imported 
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .auth import auth_views

from .exercise import exercise_views

# from .exerciseSet import exerciseSet_views

# add in the exerciseSet_views here after
views = [user_views, index_views, auth_views, exercise_views] 
# blueprints must be added to this list