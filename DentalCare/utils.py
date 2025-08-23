# For sending sms
import random
import textwrap
from io import BytesIO

from django.conf import settings
from twilio.rest import Client


def send_sms(phone_number, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    
    message = client.messages.create(
        body=message,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    print(message.sid)



import os

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils.text import slugify
# For generating profile pictures
from PIL import Image, ImageDraw, ImageFont

# def generate_profile_picture(user):
#     # Generate initials from first and last name
#     initials = f"{user.first_name[0]}{user.last_name[0]}".upper()
    
#     bg_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

#     # Create a blank image with white background
#     img = Image.new('RGB', (200, 200), color=bg_color)

#     # Draw text in the center of the image
#     d = ImageDraw.Draw(img)
#     font_path = os.path.join(settings.STATIC_URL,'fonts','Poppins-SemiBold.ttf')  # Change the font path if needed
#     font_size = 60
#     fnt = ImageFont.truetype(font_path, font_size)

#    # Calculate text bounding box
#     text_bbox = d.textbbox((0, 0), initials, font=fnt)
#     text_width = text_bbox[2] - text_bbox[0]
#     text_height = text_bbox[3] - text_bbox[1]

#     # Calculate text position
#     position = ((200 - text_width) // 2, (200 - text_height) // 2 -20)


#     # Draw text on the image
#     d.text(position, initials, font=fnt, fill=(0, 0, 0))

#     # Save the image to a BytesIO object
#     image_io = BytesIO()
#     img.save(image_io, format='PNG')
#     image_io.seek(0)

#     # Generate a unique file name
#     file_name = f"profile_{slugify(user.get_full_name())}.png"

#     # Save the image to MEDIA_ROOT/profile_pics
#     file_path = os.path.join('profile_pics', file_name)
#     file_full_path = os.path.join(settings.MEDIA_ROOT, file_path)

#     # Save the image to default storage
#     if default_storage.exists(file_full_path):
#         default_storage.delete(file_full_path)
#     default_storage.save(file_full_path, ContentFile(image_io.read()))

#     # Return the relative file path
#     return file_path

def generate_profile_picture(user):
    # Generate initials from first and last name
    initials = f"{user.first_name[0]}{user.last_name[0]}".upper()
    
    # Specify the font path
    font_path = os.path.join(settings.STATIC_ROOT, 'fonts', 'Poppins-SemiBold.ttf')
    font_size = 500
    
    # Generate profile picture image
    bg_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    img_size = (50,50)
    img = Image.new('RGB', img_size, color=bg_color)
    d = ImageDraw.Draw(img)
    
    # Load the font
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()
    
    # Calculate text position
    text_position = (20, 20)  # Adjust this position as needed
    
    # Draw text on the image
    d.text(text_position, initials, font=font, fill=(0, 0, 0))
    
    # Save the image to a BytesIO object
    image_io = BytesIO()
    img.save(image_io, format='PNG')
    image_io.seek(0)
    
    # Generate a unique file name
    file_name = f"profile_{slugify(user.get_full_name())}.png"
    
    # Save the image to MEDIA_ROOT/profile_pics
    file_path = os.path.join('profile_pics', file_name)
    file_full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    
    # Save the image to default storage
    if default_storage.exists(file_full_path):
        default_storage.delete(file_full_path)
    default_storage.save(file_full_path, ContentFile(image_io.getvalue()))
    
    # Return the relative file path
    return file_path