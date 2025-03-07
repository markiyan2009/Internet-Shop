from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField
import cloudinary.api
from django.core.files.uploadedfile import UploadedFile
from django.contrib.auth.models import Group


# Create your models here.

cloudinary.config( 
    cloud_name = "den9yj6z5", 
    api_key = "498996848524315", 
    api_secret = "kWT8gvHt4tffDaRQPqv0SADQ5bE", # Click 'View API Keys' above to copy your API secret
    secure=True
)
# For testing model validation
FILE_UPLOAD_MAX_MEMORY_SIZE = 200 * 200 * 10  # 10mb




def file_validation(file):
    if not file:
        raise ValidationError("No file selected.")

    # For regular upload, we get UploadedFile instance, so we can validate it.
    # When using direct upload from the browser, here we get an instance of the CloudinaryResource
    # and file is already uploaded to Cloudinary.
    # Still can perform all kinds on validations and maybe delete file, approve moderation, perform analysis, etc.
    if isinstance(file, UploadedFile):
        if file.size > FILE_UPLOAD_MAX_MEMORY_SIZE:
            raise ValidationError("File shouldn't be larger than 10MB.")


