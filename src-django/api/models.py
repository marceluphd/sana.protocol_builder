from django.db import models
from django.contrib.auth.models import User
from django.db import IntegrityError
import uuid


class Procedure(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    version = models.CharField(max_length=255, null=True)
    uuid = models.CharField(max_length=36, null=True)
    owner = models.ForeignKey(User)
    last_modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta():
        app_label = 'api'


class Page(models.Model):
    display_index = models.PositiveIntegerField()
    procedure = models.ForeignKey(Procedure, related_name='pages')
    last_modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, **kwargs):
        super(Page, self).save()

        self.procedure.last_modified = self.last_modified
        self.procedure.save()

    class Meta:
        app_label = 'api'
        ordering = ['procedure', 'display_index']


class Concept(models.Model):
    TYPES = (
        ('string', 'string'),
        ('boolean', 'boolean'),
        ('number', 'number'),
        ('complex', 'complex')
    )

    uuid = models.UUIDField(default=uuid.uuid4, null=False, blank=False, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    display_name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    data_type = models.CharField(max_length=16, choices=TYPES, null=True, blank=True)
    mime_type = models.CharField(max_length=128, null=True, blank=True)
    constraint = models.TextField(null=True, blank=True)

    def save(self, **kwargs):
        if self.data_type and (self.data_type, self.data_type) not in self.TYPES:
            raise IntegrityError('Invalid data type')

        super(Concept, self).save()

    class Meta:
        app_label = 'api'


class Element(models.Model):
    TYPES = (
        ('DATE', 'DATE'),
        ('ENTRY', 'ENTRY'),
        ('SELECT', 'SELECT'),
        ('MULTI_SELECT', 'MULTI_SELECT'),
        ('RADIO', 'RADIO'),
        ('PICTURE', 'PICTURE'),
        ('PLUGIN', 'PLUGIN'),
        ('ENTRY_PLUGIN', 'ENTRY_PLUGIN')
    )

    CHOICE_TYPES = (
        'SELECT',
        'MULTI_SELECT',
        'RADIO'
    )

    PLUGIN_TYPES = (
        'PLUGIN',
        'ENTRY_PLUGIN'
    )

    display_index = models.PositiveIntegerField()
    eid = models.CharField(max_length=255, null=True, blank=True)
    element_type = models.CharField(max_length=12, choices=TYPES, null=True, blank=True)
    choices = models.TextField(null=True, blank=True)
    numeric = models.CharField(max_length=255, null=True, blank=True)
    concept = models.ForeignKey(Concept, null=True, related_name='elements')
    question = models.TextField(null=True, blank=True)
    answer = models.TextField(null=True, blank=True)

    required = models.BooleanField(default=False)
    image = models.TextField(null=True, blank=True)
    audio = models.TextField(null=True, blank=True)
    action = models.TextField(null=True, blank=True)
    mime_type = models.CharField(max_length=128, null=True, blank=True)

    page = models.ForeignKey(Page, related_name='elements')
    last_modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, **kwargs):
        if self.element_type:
            if (self.element_type, self.element_type) not in self.TYPES:
                raise IntegrityError('Invalid element type')

        super(Element, self).save()

        self.page.last_modified = self.last_modified
        self.page.save()

    class Meta:
        app_label = 'api'
        ordering = ['page', 'display_index']


class ShowIf(models.Model):
    page = models.ForeignKey(Page, related_name='show_if')
    last_modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, **kwargs):
        super(ShowIf, self).save()

        self.page.last_modified = self.last_modified
        self.page.save()


class ConditionNode(models.Model):
    NODE_TYPES = (
        ('AND', 'AND'),
        ('OR', 'OR'),
        ('NOT', 'NOT'),
        ('EQUALS', 'EQUALS'),
        ('GREATER', 'GREATER'),
        ('LESS', 'LESS')
    )

    LOGICAL_TYPES = (
        'AND',
        'OR',
        'NOT'
    )

    CRITERIA_TYPES = (
        'EQUALS',
        'GREATER',
        'LESS'
    )

    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True)
    show_if = models.ForeignKey(ShowIf, on_delete=models.CASCADE, related_name='conditions', blank=True, null=True)
    criteria_element = models.ForeignKey(Element, blank=True, null=True)
    node_type = models.CharField(max_length=8, choices=NODE_TYPES)
    value = models.TextField(blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, **kwargs):
        if (self.node_type, self.node_type) not in self.NODE_TYPES:
            raise IntegrityError('Invalid condition node type')

        if self.node_type in self.CRITERIA_TYPES:
            if not self.value:
                raise IntegrityError('"CRITERIA" node type requires a value')

            if not self.criteria_element:
                raise IntegrityError('CRITERIA must have an element')

        else:
            if self.value:
                raise IntegrityError('Only "CRITERIA" should have a value')

            if self.criteria_element:
                raise IntegrityError('Only "CRITERIA" should have an element')

        if self.show_if and self.parent or (not self.show_if and not self.parent):
            raise IntegrityError('Condition node must have a parent or show_if, but not both')

        super(ConditionNode, self).save()

        if self.parent:
            self.parent.last_modified = self.last_modified
            self.parent.save()
        elif self.show_if:
            self.show_if.last_modified = self.last_modified
            self.show_if.save()

    class Meta:
        app_label = 'api'
