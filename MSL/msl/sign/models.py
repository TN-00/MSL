from django.db import models
from django.core.validators import FileExtensionValidator 
from video_encoding.fields import VideoField 
# from webcam.fields import CameraField
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile 
from webcampicture.fields import WebcamPictureField



# Label model.
class Label(models.Model):
    label_txt = models.CharField(max_length=3)
    pub_date = models.DateTimeField('data published')

    # function to return the text
    def __str__(self):
        return self.label_txt

# Signimg  model
class Signimg(models.Model):
    title = models.CharField(max_length=200, default='Sign Image')
    description = models.TextField(blank=True)
    signimg_img = models.ImageField(upload_to='signimg_images/', null=True, blank=True) 
    video = models.FileField(
        upload_to='videos/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mov', 'webm', 'jif'])]
    )
    detected_img = WebcamPictureField(
        help_text="Image captured from webcam",
        upload_to='detected_images/',
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        if self.detected_img:
            # Convert the image to a BytesIO object
            image_data = BytesIO(self.detected_img.read())
            # Process the image as needed
            # For example, you can resize or apply filters here
            # After processing, save the image back to the field
            self.detected_img = InMemoryUploadedFile(
                image_data,
                'ImageField',
                'processed_image.jpg',
                'image/jpeg',
                image_data.getbuffer().nbytes,
                None
            )
        super().save(*args, **kwargs)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    # to link Label model with signimg model through foreign key 
    label = models.ForeignKey(Label, on_delete=models.CASCADE)


# capture model to store the captured images and videos
class Capture(models.Model):
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
