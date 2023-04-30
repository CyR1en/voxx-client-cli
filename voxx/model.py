from datetime import datetime, timezone

TIME_FORMAT = "%m/%d/%y %I:%M %p"


class UID:
    TIME_EPOCH = 0x64b62a60

    def __init__(self, timestamp: int, inc_id: int):
        self._timestamp = timestamp
        self._inc_id = inc_id

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = value

    @property
    def inc_id(self):
        return self._inc_id

    @inc_id.setter
    def inc_id(self, value):
        self._inc_id = value

    def get_timestamp_string(self):
        offset_millis = self._timestamp
        dt = datetime.fromtimestamp(offset_millis / 1000, timezone.utc)
        dt_local = dt.astimezone()
        return dt_local.strftime(TIME_FORMAT)

    def get_ldt(self):
        offset_millis = self._timestamp
        return datetime.fromtimestamp(offset_millis / 1000, timezone.utc).astimezone()

    def as_long(self):
        return (self._timestamp - UID.TIME_EPOCH) << 12 | (0xFFF & self._inc_id)

    def __eq__(self, other):
        if isinstance(other, UID):
            return self._timestamp == other._timestamp and self._inc_id == other._inc_id
        return False

    def __hash__(self):
        return hash((self._timestamp, self._inc_id))

    def __str__(self):
        return f"UID: {self.as_long()} ({self._timestamp})({self._inc_id}) (ts: {self.get_timestamp_string()})"

    @staticmethod
    def of(uid: int):
        timestamp = (uid >> 12) + UID.TIME_EPOCH
        _id = uid & 0xFFF
        return UID(timestamp, _id)


class User:
    def __init__(self, uid: UID, username):
        self._uid = uid
        self._username = username

    @property
    def uid(self) -> UID:
        return self._uid

    @uid.setter
    def uid(self, uid):
        if not isinstance(uid, UID):
            raise TypeError("uid must be an instance of UID")
        self._uid = uid

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        if not isinstance(username, str):
            raise TypeError("username must be a string")
        self._username = username

    def __str__(self):
        return f"{self._username}:{self.uid.as_long()}"
