import cloudinary.uploader
# fonction pour upload une image sur cloudinary
def upload_image_to_cloudinary(request):
    img = request.FILES.get('image')
    print(img)
    if not img: 
        raise ValueError("Veuillez ajouter une image radiologique")
    try:
        uploaded_img = cloudinary.uploader.upload(img, folder='radiographie/')
    except Exception as e:
        raise ValueError("Erreur lors de l'ajout de l'image radiologique")
    print(uploaded_img.get('url'))
    return uploaded_img.get('url')