from os import getenv

from frameioclient import FrameioClient

def download(asset_id):
    token = getenv("FRAME_IO_TOKEN")
    client = FrameioClient(token)
    asset_info = client.get_asset(asset_id)
    filename = client.download(asset_info, "", prefix="", multi_part=True, concurrency=8)
    return filename


