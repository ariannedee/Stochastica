import urllib3

from pathlib import Path
from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.management.base import BaseCommand

from presentation.models import Image, Pack


class Command(BaseCommand):
    help = 'Imports all of the links in "links_list.csv" as Image objects'

    def handle(self, *args, **options):
        path = Path(settings.ENV_PATH + '/links_list.csv')
        image_urls = path.read_text().split('\n')
        http = urllib3.PoolManager()
        starter_pack = Pack.objects.first()

        images_added = 0

        for image_url in image_urls:
            if image_url.strip() == '':
                break
            filename = image_url.split('/')[-1]
            if Image.objects.filter(title=filename).exists():
                pass
            else:
                content = NamedTemporaryFile(dir=settings.MEDIA_ROOT)
                content.write(http.request('GET', image_url).data)
                i_add = Image(title=filename, pack=starter_pack)
                i_add.image.save(filename, File(content))
                content.flush()
                images_added += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully added {images_added} images'))
