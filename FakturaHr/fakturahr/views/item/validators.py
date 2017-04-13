# -*- coding: utf-8 -*-
import decimal
from colander import Schema, SchemaNode, String, null, Length, Integer, Range, Float, Decimal
from deform.widget import TextInputWidget
from fakturahr.string_constants import REQUIRED_FIELD, MAX_CHAR_LENGTH_ERROR, MIN_CHAR_LENGTH_ERROR, \
    MIN_NUMBER_RANGE_ERROR, MAX_NUMBER_RANGE_ERROR
from fakturahr.models.models import Item


class ItemNewValidator(Schema):
    name = SchemaNode(String(),
                      title=Item.NAME,
                      widget=TextInputWidget(),
                      validator=Length(min=1,
                                       max=2048,
                                       min_err=MIN_CHAR_LENGTH_ERROR.format(1),
                                       max_err=MAX_CHAR_LENGTH_ERROR.format(2048)
                                       ),
                      missing_msg=REQUIRED_FIELD
                      )
    ean = SchemaNode(String(),
                     title=Item.EAN,
                     widget=TextInputWidget(),
                     missing=null,
                     validator=Length(min=1,
                                      max=1024,
                                      min_err=MIN_CHAR_LENGTH_ERROR.format(1),
                                      max_err=MAX_CHAR_LENGTH_ERROR.format(1024)
                                      )
                     )
    measurement_unit = SchemaNode(String(),
                                  title=Item.MEASUREMENT_UNIT,
                                  widget=TextInputWidget(),
                                  missing=null,
                                  validator=Length(min=1,
                                                   max=128,
                                                   min_err=MIN_CHAR_LENGTH_ERROR.format(1),
                                                   max_err=MAX_CHAR_LENGTH_ERROR.format(128)
                                                   )
                                  )
    pack_size = SchemaNode(String(),
                           title=Item.PACK_SIZE,
                           widget=TextInputWidget(),
                           missing=null,
                           validator=Range(min=1,
                                           max=9999,
                                           min_err=MIN_NUMBER_RANGE_ERROR.format(1),
                                           max_err=MAX_NUMBER_RANGE_ERROR.format(9999)
                                           )
                           )
    pallete_size = SchemaNode(String(),
                              title=Item.PALLETE_SIZE,
                              widget=TextInputWidget(),
                              missing=null,
                              validator=Range(min=1,
                                              max=9999,
                                              min_err=MIN_NUMBER_RANGE_ERROR.format(1),
                                              max_err=MAX_NUMBER_RANGE_ERROR.format(9999)
                                              )
                              )
    price = SchemaNode(Decimal('0.01', decimal.ROUND_HALF_EVEN),
                       title=Item.PRICE,
                       widget=TextInputWidget(),
                       missing=null,
                       validator=Range(min=0,
                                       max=999999.99,
                                       min_err=MIN_NUMBER_RANGE_ERROR.format(0),
                                       max_err=MAX_NUMBER_RANGE_ERROR.format(9999)
                                       )
                       )
