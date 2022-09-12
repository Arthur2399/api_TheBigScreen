from branch.models import Branch

def NewBranch():
    branch=None
    branch_address=None
    while branch==None or branch=="":
        branch=input("Ingrese el nombre de la sucursal: ")
    while branch_address==None or branch_address=="":
        branch_address=input("Ingrese la dirección de la sucursal: ")
    branch_phone=input("Ingrese el teléfono de la sucursal (opcional): ")
    branchs=Branch()
    branchs.name_branch=branch
    branchs.address_branch=branch_address
    branchs.phone_branch=branch_phone
    branchs.save()