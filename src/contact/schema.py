import graphene
from django import forms
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphql import GraphQLError

from .models import Contact


class ContactType(DjangoObjectType):
    class Meta:
        model = Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ("name", "email", "contents")


class AddContact(DjangoModelFormMutation):
    class Meta:
        form_class = ContactForm
        return_field_name = "contact"

    @classmethod
    def perform_mutate(cls, form, info):
        if ip_address := info.context.META.get("HTTP_X_FORWARDED_FOR"):
            form.instance.ip_address = ip_address
        else:
            raise GraphQLError("IPアドレスが参照できません")
        return super().perform_mutate(form, info)


class Mutation(graphene.ObjectType):
    add_contact = AddContact.Field()
