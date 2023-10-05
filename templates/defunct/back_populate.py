from app import app
from models import db, ImageList, Image, ImagePosition 

def back_populate():
    with app.app_context(): 
        all_lists = ImageList.query.all()
        for image_list in all_lists:
            images_in_list = Image.query.filter_by(list_id=image_list.list_id).all()
            for position, image in enumerate(images_in_list, start=1):
                new_position_entry = ImagePosition(
                    image_id=image.image_id,
                    list_id=image_list.list_id,
                    position=position
                )
                db.session.add(new_position_entry)
        db.session.commit()

if __name__ == '__main__':
    back_populate()
