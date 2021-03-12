import os
import logging.config
import qrcode
import random

# Setup Logging
LOG_CONF_FILE = os.path.join(os.path.dirname(__file__),'logging.conf')
LOG_FILE = os.path.join(os.path.dirname(__file__.replace('\\','/')),'scrape.log')
logging.config.fileConfig(LOG_CONF_FILE, disable_existing_loggers=False, defaults={'logfilename': LOG_FILE})
logger = logging.getLogger(__name__)


dir_path = os.path.dirname(os.path.realpath(__file__))
# ------------------------------------------------------------------------------


qr = qrcode.QRCode(
    version=12,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=2,
    border=8
)

color_picker = ['red','green','blue','yellow','black','white']

qr.add_data('test text')
qr.make()
img = qr.make_image(fill_color=random.choice(color_picker), back_color=random.choice(color_picker))
img.save(os.path.join(dir_path,'IMAGE.png'))
logger.info("Saved Analysis script")