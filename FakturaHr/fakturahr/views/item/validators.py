# -*- coding: utf-8 -*-
import decimal
from colander import Schema, SchemaNode, String, null, Length, Integer, Range, Float, Decimal
from deform.widget import TextInputWidget
from fakturahr.string_constants import REQUIRED_FIELD, MAX_CHAR_LENGTH_ERROR, MIN_CHAR_LENGTH_ERROR, \
    MIN_NUMBER_RANGE_ERROR, MAX_NUMBER_RANGE_ERROR


class ItemNewValidator(Schema):
    name = SchemaNode(String(),
                      title=u'Ime artikla',
                      widget=TextInputWidget(),
                      validator=Length(min=1,
                                       max=2048,
                                       min_err=MIN_CHAR_LENGTH_ERROR.format(1),
                                       max_err=MAX_CHAR_LENGTH_ERROR.format(2048)
                                       ),
                      missing_msg=REQUIRED_FIELD
                      )
    ean = SchemaNode(String(),
                     title=u'EAN',
                     widget=TextInputWidget(),
                     missing=null,
                     validator=Length(min=1,
                                      max=1024,
                                      min_err=MIN_CHAR_LENGTH_ERROR.format(1),
                                      max_err=MAX_CHAR_LENGTH_ERROR.format(1024)
                                      )
                     )
    measurement_unit = SchemaNode(String(),
                                  title=u'Mjerna jedinica',
                                  widget=TextInputWidget(),
                                  missing=null,
                                  validator=Length(min=1,
                                                   max=128,
                                                   min_err=MIN_CHAR_LENGTH_ERROR.format(1),
                                                   max_err=MAX_CHAR_LENGTH_ERROR.format(128)
                                                   )
                                  )
    pack_size = SchemaNode(String(),
                           title=u'Pakiranje u kartonu',
                           widget=TextInputWidget(),
                           missing=null,
                           validator=Range(min=1,
                                           max=9999,
                                           min_err=MIN_NUMBER_RANGE_ERROR.format(1),
                                           max_err=MAX_NUMBER_RANGE_ERROR.format(9999)
                                           )
                           )
    pallete_size = SchemaNode(String(),
                              title=u'Komada na paleti',
                              widget=TextInputWidget(),
                              missing=null,
                              validator=Range(min=1,
                                              max=9999,
                                              min_err=MIN_NUMBER_RANGE_ERROR.format(1),
                                              max_err=MAX_NUMBER_RANGE_ERROR.format(9999)
                                              )
                              )
    price = SchemaNode(Decimal('0.01', decimal.ROUND_HALF_EVEN),
                       title=u'Cijena',
                       widget=TextInputWidget(),
                       missing=null,
                       validator=Range(min=1,
                                       max=9999,
                                       min_err=MIN_NUMBER_RANGE_ERROR.format(1),
                                       max_err=MAX_NUMBER_RANGE_ERROR.format(9999)
                                       )
                       )
