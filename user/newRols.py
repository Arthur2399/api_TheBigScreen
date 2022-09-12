from user.models import role

def NewRols():
    rols=[
        {'name':'Administrador',
         'description':'Administrador del sistema'
         },
        {
            'name':'Técnico',
            'description':'Gestionar funciones del sistema'
        },
        {
            'name':'Cajero',
            'description':'Accede a los modulos de "Canje" y "Creditos'
        },
        {
            'name':'Gestor de Peliculas',
            'description':'Administra las películas'
        },
        {
            'name':'Gestor de ecuestas',
            'description':'Administra las encuestas'
        }
        ]
    count=1
    for rol in rols:
        newRol=role()
        newRol.id=count
        newRol.name=rol['name']
        newRol.description=rol['description']
        newRol.save()
        count+=1