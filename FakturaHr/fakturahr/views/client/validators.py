# -*- coding: utf-8 -*-
import colander
import decimal
from fakturahr import string_constants
from colander import Schema, SchemaNode, String, null, Length
from deform.widget import TextInputWidget, HiddenWidget, SequenceWidget, MappingWidget
from fakturahr.string_constants import REQUIRED_FIELD, MAX_CHAR_LENGTH_ERROR, MIN_CHAR_LENGTH_ERROR
from fakturahr.models.models import Item

SequenceWidget.category = 'structural'

@colander.deferred
def client_item_id_validator(node, kw):
    client_item_ids = kw.get('client_item_ids')
    return colander.OneOf([client_item_id for client_item_id in client_item_ids])


class ClientNewValidator(Schema):
    name = SchemaNode(String(),
                      title=u'Ime klijenta',
                      widget=TextInputWidget(),
                      validator=Length(min=1,
                                       max=1024,
                                       min_err=MIN_CHAR_LENGTH_ERROR.format(1),
                                       max_err=MAX_CHAR_LENGTH_ERROR.format(1024)
                                       ),
                      missing_msg=REQUIRED_FIELD
                      )
    address = SchemaNode(String(),
                         title=u'Adresa klijenta',
                         widget=TextInputWidget(),
                         missing=null,
                         validator=Length(min=1,
                                          max=1024,
                                          min_err=MIN_CHAR_LENGTH_ERROR.format(1),
                                          max_err=MAX_CHAR_LENGTH_ERROR.format(1024)
                                          )
                         )
    city = SchemaNode(String(),
                      title=u'Grad klijenta',
                      widget=TextInputWidget(),
                      missing=null,
                      validator=Length(min=1,
                                       max=1024,
                                       min_err=MIN_CHAR_LENGTH_ERROR.format(1),
                                       max_err=MAX_CHAR_LENGTH_ERROR.format(1024)
                                       )
                      )
    postal_code = SchemaNode(String(),
                             title=u'Poštanski broj klijenta',
                             widget=TextInputWidget(),
                             missing=null,
                             validator=Length(min=1,
                                              max=1024,
                                              min_err=MIN_CHAR_LENGTH_ERROR.format(1),
                                              max_err=MAX_CHAR_LENGTH_ERROR.format(1024)
                                              )
                             )
    oib = SchemaNode(String(),
                     title=u'OIB klijenta',
                     widget=TextInputWidget(),
                     missing=null,
                     validator=Length(min=1,
                                      max=20,
                                      min_err=MIN_CHAR_LENGTH_ERROR.format(1),
                                      max_err=MAX_CHAR_LENGTH_ERROR.format(20)
                                      )
                     )


class ClientItemSchema(colander.Schema):
    client_item_id = colander.SchemaNode(
        colander.Integer(),
        widget=HiddenWidget(),
        validator=client_item_id_validator,
        missing_msg=REQUIRED_FIELD
    )
    name = colander.SchemaNode(
        colander.String(),
        title=Item.NAME,
        widget=TextInputWidget(
            readonly=True,
            readonly_template=u'readonly/textinput_readonly'
        ),
        missing_msg=REQUIRED_FIELD
    )
    price = colander.SchemaNode(
        colander.Decimal('0.01', decimal.ROUND_HALF_EVEN),
        title=Item.PRICE,
        missing_msg=REQUIRED_FIELD,
        widget=TextInputWidget(),
        validator=colander.Range(
            min=0,
            max=999999.99,
            min_err=string_constants.MIN_NUMBER_RANGE_ERROR.format(0),
            max_err=string_constants.MAX_NUMBER_RANGE_ERROR.format(999999.99)
        )
    )


class ClientItemSequenceSchema(colander.SequenceSchema):
    client_item = ClientItemSchema(
        widget=MappingWidget(
            template='client_items_mapping',
            item_template='client_items_mapping_item'
        )
    )


class ClientItemsSchema(colander.Schema):
    client_items = ClientItemSequenceSchema(
        widget=SequenceWidget(
            template='client_items_sequence',
            item_template='client_items_sequence_item'
        )
    )
