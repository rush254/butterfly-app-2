from azure.storage.blob import BlobServiceClient, ContentSettings, BlobClient, ContainerClient

def upload_image_to_blob(file, filename, connect_str, container_name):

    # filepath in images folder
    blob_name = f"images/{filename}"

    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    
    # Create a blob client using the folder and file name
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    # Determine the content type based on the file extension
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        content_type = 'image/jpeg'
    elif filename.lower().endswith('.gif'):
        content_type = 'image/gif'
    else:
        content_type = 'application/octet-stream'

    # Upload the blob with specified properties and metadata
    blob_client.upload_blob(
        file,
        blob_type = "BlockBlob",
        overwrite = True,
        content_settings = ContentSettings(
        content_type=content_type,
        content_language='en',
        cache_control='no-cache'),
        metadata={
            'uploaded_by': 'flask_app',
            'description': 'Uploaded image for prediction'}
    )
    
    return blob_client.url