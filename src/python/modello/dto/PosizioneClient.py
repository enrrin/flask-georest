class PosizioneClient:

    def __init__(self, ip=None, lat=None, lon=None, is_mobile=None) -> None:
        self.ip = ip
        self.lat = lat
        self.lon = lon
        self.is_mobile = is_mobile
