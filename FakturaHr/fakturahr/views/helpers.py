# -*- coding: utf-8 -*-
from fakturahr.models.database import Session
from fakturahr.models.models import Item, Client, ClientItem, Receipt, ReceiptItem


def get_item_list():
    items = Session.query(Item).filter(Item.deleted == False).all()
    return items


def get_item(item_id):
    item_object = Session.query(Item).filter(Item.id == item_id,
                                             Item.deleted == False).first()
    return item_object


def get_client_list():
    client_list = Session.query(Client).filter(Client.deleted == False).all()
    return client_list


def get_client(client_id):
    client = Session.query(Client).filter(Client.id == client_id,
                                          Client.deleted == False).first()
    return client


def get_client_list_ordered():
    client_list = Session.query(Client).filter(Client.deleted == False).order_by(Client.name.asc()).all()
    return client_list


def get_receipt_list():
    receipts = Session.query(Receipt).filter(Receipt.deleted == False).all()
    return receipts


def get_client_items(client_id):
    client_items = Session.query(ClientItem)\
        .filter(ClientItem.client_id == client_id,
                ClientItem.deleted == False).all()
    return client_items


def get_client_item(client_item_id):
    client_item = Session.query(ClientItem)\
        .filter(ClientItem.id == client_item_id,
                ClientItem.deleted == False).first()
    return client_item
