from repositories import gem_repository as gem_repo, user_repository as user_repo
from os import getenv

newuser = str(user_repo.create_new_user("GeoGemmer", str(getenv('ADMIN_PASSWORD'))))
gem_repo.create_new_gem("University of North Carolina at Charlotte", "Zoo", 35.306274, -80.734436, newuser)
gem_repo.create_new_gem("northy north trail", "Hiking Trail", 35.206274, -80.834436, newuser)
