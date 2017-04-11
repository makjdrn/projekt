from wand.image import Image

with Image(filename='Test.pdf') as img:
    with img.convert('jpg') as converted:
        converted.save(filename='Test.jpg')
