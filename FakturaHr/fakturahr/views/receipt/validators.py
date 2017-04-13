# -*- coding: utf-8 -*-
from decimal import ROUND_HALF_EVEN
import colander
from deform.widget import TextInputWidget, SelectWidget, MappingWidget, SequenceWidget
from fakturahr.string_constants import REQUIRED_FIELD, MAX_CHAR_LENGTH_ERROR, MIN_CHAR_LENGTH_ERROR, \
    MIN_NUMBER_RANGE_ERROR, MAX_NUMBER_RANGE_ERROR
from fakturahr.models.models import Item, ReceiptItem

@colander.deferred
def item_id_widget(node, kw):
    items = kw.get('items')
    return SelectWidget(values=items)

@colander.deferred
def item_id_validator(node, kw):
    items = kw.get('items')
    return colander.OneOf([item[0] for item in items])


class ReceiptItemSchema(colander.Schema):
    item_id = colander.SchemaNode(
        colander.Integer(),
        title=Item.NAME,
        widget=item_id_widget,
        validator=item_id_validator,
        missing_msg=REQUIRED_FIELD
    )

    ean = colander.SchemaNode(
        colander.String(),
        title=Item.EAN,
        widget=TextInputWidget(readonly=True),
        missing_msg=REQUIRED_FIELD
    )
    measurement_unit = colander.SchemaNode(
        colander.String(),
        title=Item.MEASUREMENT_UNIT,
        widget=TextInputWidget(readonly=True),
        missing_msg=REQUIRED_FIELD
    )
    item_price = colander.SchemaNode(
        colander.String(),
        title=Item.PRICE,
        widget=TextInputWidget(readonly=True),
        missing_msg=REQUIRED_FIELD
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
        validator=colander.Range(
            min=0,
            max=100,
            min_err=MIN_CHAR_LENGTH_ERROR.format(1),
            max_err=MAX_CHAR_LENGTH_ERROR.format(100)
        )
    )
    item_price_sum = colander.SchemaNode(
        colander.String(),
        title=Item.PRICE,
        widget=TextInputWidget(readonly=True),
        missing_msg=REQUIRED_FIELD
    )


class ReceiptItemSequence(colander.SequenceSchema):
    receipt_item = ReceiptItemSchema(
        widget=MappingWidget(
            template='receipt_item_mapping.jinja2',
            item_template='receipt_item_mapping_item.jinja2'
        )
    )


class ReceiptNewValidator(colander.Schema):
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
        colander.DateTime(),
        title=u'Datum izdavanja',
        widget=TextInputWidget(),
        missing_msg=REQUIRED_FIELD
    )
    currency_date = colander.SchemaNode(
        colander.String(),
        title=u'Datum valute plaćanja',
        widget=TextInputWidget(),
        missing_msg=REQUIRED_FIELD
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
        title=u'Cijena',
        widget=TextInputWidget(readonly=True),
        validator=colander.Range(
            min=0,
            max=999999.99,
            min_err=MIN_NUMBER_RANGE_ERROR.format(0),
            max_err=MAX_NUMBER_RANGE_ERROR.format(999999.99)
        )
    )
    tax_amount = colander.SchemaNode(
        colander.Decimal('0.01', ROUND_HALF_EVEN),
        title=u'PDV',
        widget=TextInputWidget(readonly=True),
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
        widget=TextInputWidget(readonly=True),
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
        widget=TextInputWidget(readonly=True),
        validator=colander.Range(
            min=0,
            max=999999.99,
            min_err=MIN_NUMBER_RANGE_ERROR.format(0),
            max_err=MAX_NUMBER_RANGE_ERROR.format(999999.99)
        )
    )
    payment_type = colander.SchemaNode(
        colander.String(),
        title=u'Način plaćanja',
        widget=TextInputWidget(readonly=True),
        default=u'Transakcijski račun (virman)'
    )
    operator = colander.SchemaNode(
        colander.String(),
        title=u'Operater',
        widget=TextInputWidget(readonly=True),
        default=u'Miroslav Šebrek'
    )
    receipt_items = ReceiptItemSequence(
        widget=SequenceWidget(
            min_len=1,
            template='receipt_item_sequence.jinja2',
            item_template='receipt_item_sequence_item.jinja2'
        )
    )
