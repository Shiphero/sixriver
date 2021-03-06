import enum

from datetime import datetime
from typing import List, Type
# from dataclasses import dataclass, field

from .common import Identifier, Product
from ..utils import camelcase


class GroupType(enum.Enum):

    ORDER_PICK = 'orderPick'
    BATCH_PICK = 'batchPick'


def convert_group_type(group_type):
    valid_group_types = [GroupType.ORDER_PICK, GroupType.BATCH_PICK]
    val = group_type

    if isinstance(val, str):
        val = GroupType(val)

    elif val not in valid_group_types:
        raise ValueError(f"Invalid group type, must be one of {valid_group_types}")

    return val


#@dataclass
class Pick(object):

    def __init__(
        self,
        source_location,  # str
        each_quantity,  # int
        product,  # Product
        group_type=GroupType.ORDER_PICK,  # GroupType = GroupType.ORDER_PICK
        group_id=None,  # str = None
        pick_id=None,  # str = None
        container=None,  # List['Container'] = None
        packout_container=None,  # List['Container'] = None
        destination_location=None,  # str = None
        expected_shipping_date=None,  # datetime = None
        data=None,  # dict = None
    ):
        self.group_type = convert_group_type(group_type)
        self.source_location = source_location
        self.each_quantity = each_quantity
        self.product = product
        self.group_id = group_id
        self.pick_id = pick_id
        self.container = container
        self.packout_container = packout_container
        self.destination_location = destination_location
        self.expected_shipping_date = expected_shipping_date
        self.data = data


#@dataclass
class PickComplete(object):

    def __init__(
        self,
        pick_id,  # str
        each_quantity,  # int
        source_location,  # str
        product,  # Product
        picked_quantity,  # int
        started_at=None,  # datetime
        completed_at=None,  # datetime
        reason=None,  # List[str] = None
        captured_identifiers=None,  # List[dict] = None
        user_id=None,  # str = None
        device_id=None,  # str = None
        data=None,  # dict = None
    ):
        self.started_at = started_at
        self.completed_at = completed_at
        self.pick_id = pick_id
        self.each_quantity = each_quantity
        self.source_location = source_location
        self.product = product
        self.picked_quantity = picked_quantity
        self.reason = reason
        self.captured_identifiers = captured_identifiers or []
        self.user_id = user_id
        self.device_id = device_id
        self.data = data

    @property
    def is_shortpick(self):
        return self.each_quantity != self.picked_quantity

    @property
    def rejected(self):
        return self.reason == ["REJECTED"]

    @property
    def failed(self):
        reasons = self.reason or []
        reasons = [r for r in reasons if r not in ["TAP_TO_SCAN"]]
        return len(reasons) > 0

    @property
    def barcodes(self):
        return {e["barcode"]: e.get("quantity") for e in self.captured_identifiers if "barcode" in e}


#@dataclass
class PickTaskPicked(object):

    def __init__(
        self,
        timestamp,  # datetime
        pick_id,  # str
        group_id,  # str
        group_type,  # GroupType
        container,  # Type['Container']
        induct,  # Type['Induct']
        picks,  # List[PickComplete]
        user_id=None,  # str = None
        device_id=None,  # str = None
        data=None,  # str = None
    ):
        self.group_type = convert_group_type(group_type)
        self.timestamp = timestamp
        self.pick_id = pick_id
        self.group_id = group_id
        self.container = container
        self.induct = induct
        self.picks = picks
        self.user_id = user_id
        self.device_id = device_id
        self.data = data

    @property
    def has_errors(self):
        return any(pc.failed for pc in self.picks)

    @property
    def short_picks(self):
        return [p for p in self.picks if p.failed]
