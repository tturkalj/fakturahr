# -*- coding: utf-8 -*-
from colander import Schema, SchemaNode, String, null, Length
from deform.widget import TextInputWidget
from fakturahr.string_constants import REQUIRED_FIELD, MAX_CHAR_LENGTH_ERROR, MIN_CHAR_LENGTH_ERROR


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
