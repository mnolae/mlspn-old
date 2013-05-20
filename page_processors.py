from mezzanine.galleries.models import Gallery

def all_galleries(request):
    galleries = Gallery.objects.all()
    return {'pages': galleries}