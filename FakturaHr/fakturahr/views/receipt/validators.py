# -*- coding: utf-8 -*-
import colander
from decimal import ROUND_HALF_EVEN
from datetime import datetime
from deform.widget import TextInputWidget, SelectWidget, MappingWidget, SequenceWidget
from fakturahr.string_constants import REQUIRED_FIELD, MAX_CHAR_LENGTH_ERROR, MIN_CHAR_LENGTH_ERROR, \
    MIN_NUMBER_RANGE_ERROR, MAX_NUMBER_RANGE_ERROR
from fakturahr.models.models import Item, ReceiptItem, Receipt

@colander.deferred
def item_id_widget(node, kw):
    items = kw.get('items')
    return SelectWidget(values=items, css_class='input-medium')

@colander.deferred
def item_id_validator(node, kw):
    items = kw.get('items')
    return colander.OneOf([item[0] for item in items])


@colander.deferred
def client_id_widget(node, kw):
    clients = kw.get('clients')
    return SelectWidget(values=clients, css_class='input-medium')

@colander.deferred
def client_id_validator(node, kw):
    clients = kw.get('clients')
    return colander.OneOf([client[0] for client in clients])

@colander.deferred
def payment_type_widget(node, kw):
    payment_types = kw.get('payment_types')
    return SelectWidget(values=payment_types, css_class='input-medium')

@colander.deferred
def payment_type_validator(node, kw):
    payment_types = kw.get('payment_types')
    return colander.OneOf([payment_type[0] for payment_type in payment_types])


def validate_date(node, value):
    try:
        parsed_date = datetime.strptime(value, Receipt.date_format)
    except:
        raise colander.Invalid(node, u'Pogrešan format datuma!')


class ReceiptItemSchema(colander.Schema):
    client_item_id = colander.SchemaNode(
        colander.Integer(),
        title=Item.NAME,
        widget=item_id_widget,
        validator=item_id_validator,
        missing_msg=REQUIRED_FIELD
    )
    ean = colander.SchemaNode(
        colander.String(),
        title=Item.EAN,
        widget=TextInputWidget(
            readonly=True,
            readonly_template=u'readonly/textinput_readonly'
        ),
        missing_msg=REQUIRED_FIELD
    )
    measurement_unit = colander.SchemaNode(
        colander.String(),
        title=Item.MEASUREMENT_UNIT,
        widget=TextInputWidget(
            readonly=True,
            readonly_template=u'readonly/textinput_readonly'
        ),
        missing_msg=REQUIRED_FIELD
    )
    item_price = colander.SchemaNode(
        colander.Decimal('0.01', ROUND_HALF_EVEN),
        title=Item.PRICE,
        missing_msg=REQUIRED_FIELD,
        widget=TextInputWidget(
            readonly=True,
            readonly_template=u'readonly/textinput_readonly'
        ),
        validator=colander.Range(
            min=0,
            max=999999.99,
            min_err=MIN_NUMBER_RANGE_ERROR.format(0),
            max_err=MAX_NUMBER_RANGE_ERROR.format(999999.99)
        )
    )
    quantity = colander.SchemaNode(
        colander.Integer(),
        title=ReceiptItem.QUANTITY,
        widget=TextInputWidget(),
        missing_msg=REQUIRED_FIELD,
        validator=colander.Range(
            min=1,
            max=9999,
            min_err=MIN_CHAR_LENGTH_ERROR.format(1),
            max_err=MAX_CHAR_LENGTH_ERROR.format(9999)
        )
    )
    rebate_percent = colander.SchemaNode(
        colander.Float(),
        title=ReceiptItem.REBATE_PERCENT,
        widget=TextInputWidget(),
        missing_msg=REQUIRED_FIELD,
        default=0.0,
        validator=colander.Range(
            min=0,
            max=100,
            min_err=MIN_CHAR_LENGTH_ERROR.format(1),
            max_err=MAX_CHAR_LENGTH_ERROR.format(100)
        )
    )

    item_price_sum = colander.SchemaNode(
        colander.Decimal('0.01', ROUND_HALF_EVEN),
        title=Item.PRICE_SUM,
        missing_msg=REQUIRED_FIELD,
        widget=TextInputWidget(
            readonly=True,
            readonly_template=u'readonly/textinput_readonly'
        ),
        validator=colander.Range(
            min=0,
            max=999999.99,
            min_err=MIN_NUMBER_RANGE_ERROR.format(0),
            max_err=MAX_NUMBER_RANGE_ERROR.format(999999.99)
        )
    )


class ReceiptItemSequence(colander.SequenceSchema):
    receipt_item = ReceiptItemSchema(
        widget=MappingWidget(
            template='receipt_item_mapping.jinja2',
            item_template='receipt_item_mapping_item.jinja2'
        )
    )


class ReceiptBaseValidator(colander.Schema):
    number = colander.SchemaNode(
        colander.String(),
        title=u'Broj računa',
        widget=TextInputWidget(),
        missing_msg=REQUIRED_FIELD,
        validator=colander.Length(
            min=1,
            max=100,
            min_err=MIN_CHAR_LENGTH_ERROR.format(1),
            max_err=MAX_CHAR_LENGTH_ERROR.format(100)
        )
    )
    issued_date = colander.SchemaNode(
        colander.String(),
        title=u'Datum izdavanja',
        widget=TextInputWidget(),
        missing_msg=REQUIRED_FIELD,
        validator=validate_date
    )
    currency_date = colander.SchemaNode(
        colander.String(),
        title=u'Datum valute plaćanja',
        widget=TextInputWidget(),
        missing_msg=REQUIRED_FIELD,
        validator=validate_date
    )
    issued_time = colander.SchemaNode(
        colander.String(),
        title=u'Vrijeme izdavanja',
        widget=TextInputWidget(),
        missing_msg=REQUIRED_FIELD,
        validator=colander.Length(
            min=1,
            max=10,
            min_err=MIN_CHAR_LENGTH_ERROR.format(1),
            max_err=MAX_CHAR_LENGTH_ERROR.format(10)
        )
    )
    issued_location = colander.SchemaNode(
        colander.String(),
        title=u'Mjesto izdavanja',
        widget=TextInputWidget(),
        missing_msg=REQUIRED_FIELD,
        validator=colander.Length(
            min=1,
            max=100,
            min_err=MIN_CHAR_LENGTH_ERROR.format(1),
            max_err=MAX_CHAR_LENGTH_ERROR.format(100)
        )
    )
    base_amount = colander.SchemaNode(
        colander.Decimal('0.01', ROUND_HALF_EVEN),
        title=u'Osnovica za {0}%'.format(Receipt.TAX_PERCENT),
        missing_msg=REQUIRED_FIELD,
        widget=TextInputWidget(
            readonly=True,
            readonly_template=u'readonly/textinput_readonly'
        ),
        validator=colander.Range(
            min=0,
            max=999999.99,
            min_err=MIN_NUMBER_RANGE_ERROR.format(0),
            max_err=MAX_NUMBER_RANGE_ERROR.format(999999.99)
        )
    )
    tax_amount = colander.SchemaNode(
        colander.Decimal('0.01', ROUND_HALF_EVEN),
        title=u'PDV {0}%'.format(Receipt.TAX_PERCENT),
        missing_msg=REQUIRED_FIELD,
        widget=TextInputWidget(
            readonly=True,
            readonly_template=u'readonly/textinput_readonly'
        ),
        validator=colander.Range(
            min=0,
            max=999999.99,
            min_err=MIN_NUMBER_RANGE_ERROR.format(0),
            max_err=MAX_NUMBER_RANGE_ERROR.format(999999.99)
        )
    )
    return_amount = colander.SchemaNode(
        colander.Decimal('0.01', ROUND_HALF_EVEN),
        title=u'Povratna naknada',
        widget=TextInputWidget(
            readonly=True,
            readonly_template=u'readonly/textinput_readonly'
        ),
        missing_msg=REQUIRED_FIELD,
        validator=colander.Range(
            min=0,
            max=999999.99,
            min_err=MIN_NUMBER_RANGE_ERROR.format(0),
            max_err=MAX_NUMBER_RANGE_ERROR.format(999999.99)
        )
    )
    total_amount = colander.SchemaNode(
        colander.Decimal('0.01', ROUND_HALF_EVEN),
        title=u'UKUPNO',
        missing_msg=REQUIRED_FIELD,
        widget=TextInputWidget(
            readonly=True,
            readonly_template=u'readonly/textinput_readonly'
        ),
        validator=colander.Range(
            min=0,
            max=999999.99,
            min_err=MIN_NUMBER_RANGE_ERROR.format(0),
            max_err=MAX_NUMBER_RANGE_ERROR.format(999999.99)
        )
    )
    payment_type = colander.SchemaNode(
        colander.Integer(),
        title=u'Način plaćanja',
        default=Receipt.SLIP,
        missing_msg=REQUIRED_FIELD,
        widget=payment_type_widget,
        validator=payment_type_validator
    )
    operator = colander.SchemaNode(
        colander.String(),
        title=u'Operater',
        missing_msg=REQUIRED_FIELD,
        widget=TextInputWidget(
            readonly=True,
            readonly_template=u'readonly/textinput_readonly'
        )
    )
    receipt_items = ReceiptItemSequence(
        widget=SequenceWidget(
            min_len=1,
            template='receipt_item_sequence.jinja2',
            item_template='receipt_item_sequence_item.jinja2'
        )
    )


class ReceiptNewValidator(ReceiptBaseValidator):
    client_id = colander.SchemaNode(
        colander.Integer(),
        title=Receipt.CLIENT,
        widget=client_id_widget,
        validator=client_id_validator,
        missing_msg=REQUIRED_FIELD,
        insert_before='number'
    )


class ReceiptEditValidator(ReceiptBaseValidator):
    client_name = colander.SchemaNode(
        colander.String(),
        title=Receipt.CLIENT,
        widget=TextInputWidget(
            readonly=True,
            readonly_template=u'readonly/textinput_readonly'
        ),
        missing_msg=REQUIRED_FIELD,
        insert_before='number'
    )
