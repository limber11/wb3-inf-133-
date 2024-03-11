from graphene import objecType, String, Int, List, Schema, Field

class Query(ObjecType):
    estudiantes = List(Estudiantes)
    estudiantes_por_Id = Field(Estudiante, id = int())



    def resolve_estudiante_por_id(root, info, id):
        for estudiante in estudiante:
            if estudiante.id == id:
                 return estudiante
            return None