from django.db import models
from django.core.files import File
from PIL import Image, ImageOps
from io import BytesIO

from utils.validators import validate_image
from utils.file_dir import Candidate_Profile_Images, Category_Profile_Images

class CategoryModel(models.Model):

    class Meta:
        ordering = ['id']

    category_name = models.CharField(null=False, blank=True, max_length=256)
    category_description = models.CharField(
        null=True, blank=True, max_length=4096)
    category_coverImage = models.ImageField(null=False, blank=True, upload_to=Category_Profile_Images, validators=[validate_image])
    is_top_category = models.BooleanField(null=False, blank=False, default=False)
    encoder_ID = models.CharField(null=False, blank=True, max_length=1023)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        image = Image.open(self.category_coverImage)
        image = image.convert('RGB')
        image = ImageOps.exif_transpose(image)
        image_io = BytesIO()
        image.save(image_io, "JPEG", optimize=True, quality=50)
        compressed_image = File(image_io, name=str(self.category_coverImage))
        self.category_coverImage = compressed_image
        super(CategoryModel, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.pk}-{self.category_name}"

class CandidateModel(models.Model):

    class Meta:
        ordering = ['id']

    candidate_name = models.CharField(null=False, blank=True, max_length=256)
    candidate_description = models.CharField(
        null=True, blank=True, max_length=4096)
    candidate_profileImage = models.ImageField(null=False, blank=True, upload_to=Candidate_Profile_Images, validators=[validate_image])
    category = models.ManyToManyField(CategoryModel, related_name="candidates")
    encoder_ID = models.CharField(null=False, blank=True, max_length=1023)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        image = Image.open(self.candidate_profileImage)
        image = image.convert('RGB')
        image = ImageOps.exif_transpose(image)
        image_io = BytesIO()
        image.save(image_io, "JPEG", optimize=True, quality=50)
        compressed_image = File(
            image_io, name=str(self.candidate_profileImage))
        self.candidate_profileImage = compressed_image
        super(CandidateModel, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.pk}-{self.candidate_name}"

class VoteModel(models.Model):
    
    class Meta:
        ordering = ['id']
        
    category = models.ForeignKey(CategoryModel, on_delete=models.DO_NOTHING)
    candidate = models.ForeignKey(CandidateModel, on_delete=models.DO_NOTHING)
    
    # Votter info start
    ipv4 = models.GenericIPAddressField(blank=False, null=False, default="0.0.0.0")
    finger_print = models.CharField(blank=False, null=False, default="finger_print")
    # Votter info end
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)