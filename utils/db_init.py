from models.base import db
from models.service import Service

db.drop_all()
db.create_all()

# create services
service_list = []
for tmp in [
        "Beauticians",
        "Carpenters",
        "ComputerTechnicians",
        "Electricians",
        "Gardeners",
        "Laborers",
        "Masseuses",
        "Painters",
        "Plumbers",
        "Therapists"]:
    service = Service()
    service.name = tmp
    service_list.append(service)
    db.session.add(service)

db.session.commit()
