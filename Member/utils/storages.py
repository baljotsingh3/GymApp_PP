
# from storages.backends.s3boto3 import S3Boto3Storage
# from django.core.files.base import ContentFile

# # Initialize the storage backend
# def upload_media(image_content,file_name):
# # Open the image file
#     # with open(file_path, 'rb') as f:
#     #     image_content = f.read()

# # Initialize the storage
#     storage = S3Boto3Storage()

# # Create a ContentFile object from the image bytes

#     file_content = ContentFile(image_content.read())

#     # Save the image to storage
#      # You can change this path if you want
#     saved_name = storage.save(file_name, file_content)

#     # Get the URL
#     file_url = storage.url(saved_name)

#     print("Image uploaded as:", saved_name)
#     print("Image URL:", file_url)
    
#     return file_url
