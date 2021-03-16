from frameioclient import FrameioClient
from os import getenv

def add_metadata(asset_id,metadata):
    token = getenv("FRAME_IO_TOKEN")
    client = FrameioClient(token)
    client.update_asset(asset_id, description=metadata)
