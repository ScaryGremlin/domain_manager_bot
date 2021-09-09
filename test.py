import miscellaneous as misc

fio = "Джемакулов Артур Александрович"
org_unit = "back_office"
DOMAIN = "CO.MFCMGO.RU"


surname, name, _, login = misc.requisites_to_data(fio)
cn = f"CN={name} {surname},"
ou = f"OU={org_unit},"
dc = ",".join([f"DC={element}" for element in DOMAIN.split(".")])
dn = cn + ou + dc
print(dn)
