from routes.account import blp as AccountBlueprint
from routes.profile import blp as ProfileBlueprint
from routes.cv import blp as CvBlueprint
from routes.job_post import blp as JobPostBlueprint
from routes.user_membership import blp as UserMembershipBlueprint
from routes.user_application_management import blp as UserApplicationBlueprint
from routes.business_application_management import blp as BusinessApplicantBlueprint
from routes.bookmark import blp as BookmarkBlueprint

# public routes
from routes.public.jobs import blp as JobsBlueprint
from routes.public.featured_jobs import blp as FeaturedJobsBlueprint