from typing_extensions import Required
import graphene
from graphene.types import schema
from graphene_django import DjangoObjectType, fields
from .models import Note

class NoteType(DjangoObjectType):
    class Meta:
        model = Note
        fields = ('id','title','content')

class Query(graphene.ObjectType):

    all_notes = graphene.List(NoteType)

    def resolve_all_notes(root,info):
        return Note.objects.all()


#___________Creating new data__________


class CreateNote(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required = True)

    note = graphene.Field(NoteType)

    @classmethod
    def mutate(cls,root,info,title,content):
        note = Note(title=title,content=content)
        note.save()
        return CreateNote(note=note)



#____________Updating data_________


class UpdateNote(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        title = graphene.String(required=True)
        content = graphene.String(required = True)

    note = graphene.Field(NoteType)

    @classmethod
    def mutate(cls,root,info,title,content,id):
        note = Note.objects.get(id=id)
        note.title = title
        note.content = content
        note.save()
        return UpdateNote(note=note)


#____Deleting the data_______


class DeleteNote(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        title = graphene.String(required=True)
        # content = graphene.String(required = True)

    note = graphene.Field(NoteType)

    @classmethod
    def mutate(cls,root,info,id,title):
        note = Note.objects.get(id=id)
        note.title = title
        note.delete()
        return


class Mutation(graphene.ObjectType):
    delete_Notes = DeleteNote.Field()
    create_notes = CreateNote.Field()
    update_notes = UpdateNote.Field()


schema = graphene.Schema(query=Query,mutation=Mutation)
