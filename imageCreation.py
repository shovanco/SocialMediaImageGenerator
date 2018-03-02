from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageOps
from urllib import request
import io
import textwrap
import csv
import os

class SocialMediaImageAutomation:

    """
    This class is used to generate social media images based on a CSV data source
    and output type which is one of a few preset options.
    """

    def __init__(self, data_src_file_name, media_templates, local_file_folder="resources/",output_path="social-media/"):

        # Verbose output toggle
        self.verbose = True
        # Verbose output toggle
        self.common_image = "https://hkg18.pathable.com/assets/user/full-011dbf1dff775b23f0f853f4f9aac853.gif"
        # Get the data source csv file
        self._data_src_file_name = data_src_file_name
        # Local resources directory pathdrive
        self.local_resources_path = local_file_folder
        # Local images
        self.local_images = {
            "HKG18-300K1": "Leendert-van-Doorn.jpg",
            "HKG18-500K2": "laura-dekker.jpg"
        }
        # Local Output path for images
        self.output_path = os.getcwd() + "/" + output_path
        # Local Output path for images
        self.second_output_path = os.getcwd() + "/" + "video/"
        # Circle Thumbnail Size
        self.circle_thumb_size = (300, 300)

        # Define the keys and their column numbers in the spreadsheet
        self.user_input = {
                            "title":4,
                            "session_id":0,
                            "position":11,
                            "speakers":10,
                            "tracks":9,
                            "photo":13,
                            "keywords":18,
                            "emails": 12
                            }

        self.types = ["HKG18-Video-Placeholder-BG.jpg", "HKG18-Social-Media-bg.jpg"]

        # Youtube Thumbnail Image URl
        self.youtube_thumbnail_image = "https://img.youtube.com/vi/{0}/sddefault.jpg"

        # Background image template
        self.template_images = media_templates


        # Positions of elements
        self.photo_offset = (900,400)
        self.title_offset = [70,240]
        self.keywords_offset = [70,440]
        self.track_offset = [70,200]
        self.name_offset = [940,70]
        self.position_offset = [940,130]
        self.event_hash_tag_offset = [[500,750],120]
        
        
        # Positions of elements
        self.second_photo_offset = (900,20)
        self.second_title_offset = [28,210]
        self.second_keywords_offset = [30,440]
        self.second_track_offset = [30,183]
        self.second_name_offset = [940,70]
        self.second_position_offset = [940,130]
        self.second_event_hash_tag_offset = [[500,750],120]


        self.event_hash_tag = "#HKG18"

        self.fonts = {"regular":"Lato-Regular.ttf",
                      "bold":"Lato-Bold.ttf"}

        self.colours = {"black":(0,0,0),
                        "white":(255,255,255),
                        "grey":(153,153,153),
                        "linaro-blue":(70,145,218),
                        "linaro-green":(164,203,64)}

        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

        self.csv_data = self.grab_data_from_csv()


        for template in self.template_images:
            # print(self.csv_data)
            self.create_social_media_images(template)


    def grab_data_from_csv(self):

        my_file = self._data_src_file_name
        with open(my_file, 'rt',encoding="utf8") as f:
            reader = csv.reader(f)
            csv_data = list(reader)
            data = []
            for each in csv_data:

                title = each[self.user_input["title"]]
                session_id = each[self.user_input["session_id"]]
                position = each[self.user_input["position"]]
                speaker_names = each[self.user_input["speakers"]]
                keywords = each[self.user_input["keywords"]]
                track = each[self.user_input["tracks"]]
                emails = each[self.user_input["emails"]]
                if "://" in each[self.user_input["photo"]]:
                    photo = each[self.user_input["photo"]]
                else:
                    photo = ""

                new_list = [title,speaker_names,track,photo,position,session_id,keywords,emails]
                data.append(new_list)
            # for each in data:
            #     print(each)

        return data


    def write_text(self, background_image_draw, text, coords, font_size, font, colour, centered=False, multiline=False, wrap_width=28):

        image_font = ImageFont.truetype(font, font_size)

        text_width, text_height = image_font.getsize(text)

        text_y = coords[1]

        if centered:
            x = coords[0][0]
            x2 = coords[0][1]
            text_x = x + ((x2 - x) - (text_width) / 2)
        else:
            text_x = coords[0]

        text_coords = (text_x,text_y)

        if not multiline:
            background_image_draw.text(text_coords, text, colour, font=image_font)
        else:
            # Convert the text into multiple lines
            lines = textwrap.wrap(text, width=wrap_width)
            line_y = text_coords[1]
            for line in lines:
                width, height = image_font.getsize(line)
                background_image_draw.text((text_coords[0],line_y), line, colour, font=image_font)
                line_y += height

        return background_image_draw


    def create_social_media_images(self, media_template):


        for speaker in self.csv_data:

            title = speaker[0]
            name = speaker[1]
            track = speaker[2]
            image_name = speaker[3]
            position = speaker[4]
            session_id = speaker[5]
            keywords = speaker[6]
            emails = speaker[7]

            print("Session ID: {0}".format(session_id))
            print("Session Title: {0}".format(title))
            print("Speaker Name: {0}".format(name))
            print("Track: {0}".format(track))
            print("Speaker Image: {0}".format(image_name))
            print("Speaker Position: {0}".format(position))
            print("Keywords: {0}".format(keywords))
            print("Emails: {0}".format(emails))

            if title == "" or session_id == "":
                pass
            else:
                print("Image Name:",image_name)
                print("Common Image:",self.common_image)
                if name == "":
                    name = session_id
                if session_id in self.local_images:
                    image_file_name = self.local_resources_path + self.local_images[session_id]
                else:
                    if image_name == self.common_image:
                        image_file_name = False
                    elif "://" in image_name:
                        image_file_name = self.grab_photo(image_name)
                    elif image_name == "":
                        image_file_name = False
                    else:
                        image_file_name = self.local_resources_path + image_name

                print("IMAGE: {0}".format(image_file_name))

                background_image = Image.open(media_template).convert("RGBA")

                background_width, background_height = background_image.size


        
                if media_template in self.types:
                    if media_template == self.types[0]:
                        
                        if image_file_name != False:
                            thumbnail = self.create_normal_thumbnail(image_file_name, 300)
                    
                            # Paste the generated circular thumbnail.
                            speaker_image_w, speaker_image_h = thumbnail.size
                            speaker_image_offset_calculated = [background_width - (speaker_image_w + 60), background_height - speaker_image_h]
                            background_image.paste(thumbnail, speaker_image_offset_calculated, thumbnail)

                        if keywords:
                            if keywords == "keywords":
                                actual_keywords = False
                            elif keywords == "":
                                actual_keywords = False
                            else:
                                actual_keywords = keywords.split(",")

                        # Get the draw object from ImageDraw.Draw() method
                        background_image_draw = ImageDraw.Draw(background_image)
                        # Video Generation
                        # Generate blue overlay
                        email_string = ""
                        if name == "Not Found":
                            split_emails = emails.split(",")
                            count = 0
                            for email in split_emails:
                                if count == 0:
                                    email_string = email
                                else:
                                    email_string = email_string + ", " + email
                                count += 1
                                    
                            email_font  = ImageFont.truetype(self.fonts["bold"], 20)
                            email_w, email_h = email_font.getsize(email_string)
                            x_offset = (background_width - email_w) - 60
                            email_offset_calculated = [x_offset , 70]
                            background_image_draw = self.write_text(background_image_draw, email_string, email_offset_calculated, 20, self.fonts["bold"], self.colours["white"])
                        else:
                            # Speaker Name
                            if len(name) < 40:
                                name_font  = ImageFont.truetype(self.fonts["bold"], 27)
                                name_w, name_h = name_font.getsize(name)
                                name_offset_calculated = [background_width - (name_w + 60), 70]

                                print("Calculated Name Width:", name_w)
                                print("Calculated Offset: ", name_offset_calculated)
                                background_image_draw = self.write_text(background_image_draw, name, name_offset_calculated, 27, self.fonts["bold"], self.colours["white"])
                            else:
                                background_image_draw = self.write_text(background_image_draw, name,self.name_offset,20, self.fonts["bold"], self.colours["white"])
                        
                        
                        # Session ID -----------
                        if position == "Not Found":
                            session_id_font  = ImageFont.truetype(self.fonts["regular"], 27)
                            session_id_w, session_id_h = session_id_font.getsize(session_id)
                            x_offset = (background_width - session_id_w) - 60
                            session_id_offset_calculated = [x_offset , 130]
                            
                            background_image_draw = self.write_text(background_image_draw, session_id, session_id_offset_calculated,27, self.fonts["regular"], self.colours["white"])
                        else:
                            # Speaker Position
                            if len(position) < 40:
                                position_font  = ImageFont.truetype(self.fonts["regular"], 27)
                                position_w, position_h = position_font.getsize(position)
                                x_offset = (background_width - position_w) - 60
                                position_offset_calculated = [x_offset , 130]
                                background_image_draw = self.write_text(background_image_draw, position,position_offset_calculated,27, self.fonts["regular"], self.colours["white"])
                            else:
                                position_font_smaller  = ImageFont.truetype(self.fonts["regular"], 20)
                                position_w_smaller, position_h_smaller = position_font_smaller.getsize(position)
                                x_offset = (background_width - position_w_smaller) - 60
                                position_offset_calculated_new = [x_offset , 130]
                                background_image_draw = self.write_text(background_image_draw, position,position_offset_calculated_new,20, self.fonts["regular"], self.colours["white"])
                        

                        # Session Track
                        background_image_draw = self.write_text(background_image_draw, track, self.track_offset, 26, self.fonts["bold"], self.colours["white"])

                        # Session Title
                        if len(title) < 40:
                            background_image_draw = self.write_text(background_image_draw, title,self.title_offset, 72, self.fonts["bold"], self.colours["white"], multiline=True)
                        else:
    
                            background_image_draw = self.write_text(background_image_draw, title,self.title_offset, 56, self.fonts["bold"], self.colours["white"], multiline=True)
                            
                        

                        # Keywords
                        if actual_keywords:
                            counter = 0
                            keyword_offset = []
                            for word in actual_keywords[0:3]:

                                keyword_font = ImageFont.truetype(self.fonts["bold"], 44)

                                text_width, text_height = keyword_font.getsize(word)

                                keyword_offset = self.keywords_offset
                                keyword_offset[1] = background_height - 170
                                background_image_draw = self.write_text(background_image_draw, "#" + word,keyword_offset, 44, self.fonts["regular"], self.colours["linaro-green"])
                                keyword_offset[0] = keyword_offset[0] + (text_width + 50)
                                counter += 1

                        # Event Hash Tag - If not speaker Image
                        # if not image_file_name:
                        #     background_image_draw = self.write_text(background_image_draw, self.event_hash_tag,self.event_hash_tag_offset,44, self.fonts["bold"], self.colours["linaro-blue"], centered=True)


                        output_file = self.output_path + session_id.lower() + ".png"
                        print(output_file)
                        # Save the final image.
                        background_image.save(output_file, quality=95)

                    elif media_template == self.types[1]:
                        
                        # Add the profile photo
                        
                        if image_file_name:
                            
                            thumbnail = self.create_normal_thumbnail(image_file_name, 200)

                            # Paste the generated circular thumbnail.
                            speaker_image_w, speaker_image_h = thumbnail.size
                            speaker_image_offset_calculated = [background_width - 300, 20]
                            background_image.paste(thumbnail, speaker_image_offset_calculated, thumbnail)

                        if keywords:
                            if keywords == "keywords":
                                actual_keywords = False
                            elif keywords == "":
                                actual_keywords = False
                            else:
                                actual_keywords = keywords.split(",")

                        # Get the draw object from ImageDraw.Draw() method
                        background_image_draw = ImageDraw.Draw(background_image)
                        
                        
                        # Video Generation
                        # Generate blue overlay
                        email_string = ""
                        if name == "Not Found":
                            split_emails = emails.split(",")
                            count = 0
                            for email in split_emails:
                                if count == 0:
                                    email_string = email
                                else:
                                    email_string = email_string + ", " + email
                                count += 1
                                    
                            email_font  = ImageFont.truetype(self.fonts["bold"], 20)
                            email_w, email_h = email_font.getsize(email_string)
                            x_offset = (background_width - email_w) - 60
                            email_offset_calculated = [x_offset , 70]
                            background_image_draw = self.write_text(background_image_draw, email_string, email_offset_calculated, 20, self.fonts["bold"], self.colours["white"])
                        else:
                            # Speaker Name
                            if len(name) < 40:
                                name_font  = ImageFont.truetype(self.fonts["bold"], 27)
                                name_w, name_h = name_font.getsize(name)
                                name_offset_calculated = [background_width - (name_w + 60), 70]

                                print("Calculated Name Width:", name_w)
                                print("Calculated Offset: ", name_offset_calculated)
                                background_image_draw = self.write_text(background_image_draw, name, name_offset_calculated, 27, self.fonts["bold"], self.colours["white"])
                            else:
                                background_image_draw = self.write_text(background_image_draw, name,self.second_name_offset,20, self.fonts["bold"], self.colours["white"])
                        
                        
                        # Session ID -----------
                        if position == "Not Found":
                            session_id_font  = ImageFont.truetype(self.fonts["regular"], 27)
                            session_id_w, session_id_h = session_id_font.getsize(session_id)
                            x_offset = (background_width - session_id_w) - 60
                            session_id_offset_calculated = [x_offset , 130]
                            
                            background_image_draw = self.write_text(background_image_draw, session_id, session_id_offset_calculated,27, self.fonts["regular"], self.colours["white"])
                        else:
                            # Speaker Position
                            if len(position) < 40:
                                position_font  = ImageFont.truetype(self.fonts["regular"], 27)
                                position_w, position_h = position_font.getsize(position)
                                x_offset = (background_width - position_w) - 60
                                position_offset_calculated = [x_offset , 130]
                                background_image_draw = self.write_text(background_image_draw, position,position_offset_calculated,27, self.fonts["regular"], self.colours["white"])
                            else:
                                position_font_smaller  = ImageFont.truetype(self.fonts["regular"], 20)
                                position_w_smaller, position_h_smaller = position_font_smaller.getsize(position)
                                x_offset = (background_width - position_w_smaller) - 60
                                position_offset_calculated_new = [x_offset , 130]
                                background_image_draw = self.write_text(background_image_draw, position,position_offset_calculated_new,20, self.fonts["regular"], self.colours["white"])
                        

                        # Session Track
                        background_image_draw = self.write_text(background_image_draw, track, self.second_track_offset, 16, self.fonts["bold"], self.colours["white"])

                        # Session Title
                        if len(title) < 40:
                            background_image_draw = self.write_text(background_image_draw, title,self.second_title_offset, 34, self.fonts["bold"], self.colours["white"], multiline=True)
                        else:
    
                            background_image_draw = self.write_text(background_image_draw, title,self.second_title_offset, 30, self.fonts["bold"], self.colours["white"], multiline=True)
                            
                        # Keywords
                        if actual_keywords:
                            counter = 0
                            keyword_offset = []
                            for word in actual_keywords[0:3]:

                                keyword_font = ImageFont.truetype(self.fonts["bold"], 44)
                                text_width, text_height = keyword_font.getsize(word)
                                keyword_offset = self.second_keywords_offset
                                keyword_offset[1] = background_height - 170
                                background_image_draw = self.write_text(background_image_draw, "#" + word,keyword_offset, 44, self.fonts["regular"], self.colours["linaro-green"])
                                keyword_offset[0] = keyword_offset[0] + (text_width + 50)
                                counter += 1

                        # Event Hash Tag - If not speaker Image
                        # if not image_file_name:
                        #     background_image_draw = self.write_text(background_image_draw, self.event_hash_tag,self.event_hash_tag_offset,44, self.fonts["bold"], self.colours["linaro-blue"], centered=True)

                        output_file = self.second_output_path + session_id.lower() + ".png"
                        print(output_file)
                        # Save the final image.
                        background_image.save(output_file, quality=95)

    def grab_photo(self, url):

        speaker_image_file_name = url.split("/")[-1]
        speaker_image_file_name = speaker_image_file_name.split("?")[0]

        try:
            speaker_image = request.urlretrieve(url, speaker_image_file_name)
            if self.verbose:
                print("Image successfully retreived: {0}".format(speaker_image_file_name))
        except Exception as e:
            if self.verbose:
                print("Failed to grab image - {0}".format(e))
            return False

        return speaker_image_file_name

    def create_circle_thumbnail(self, file_name):


        # Open the speaker image to generate the circular thumb.
        image_obj = Image.open(file_name)
        # Create a circle thumbnail file name
        circle_thumbnail_file_name = '{0}-{1}.png'.format(file_name,"circle")
        # Create a new circle thumb mask
        mask = Image.new('L', self.circle_thumb_size, 0)
        # Instantiate Draw() for mask.
        draw = ImageDraw.Draw(mask)
        # Draw a circle with set size and fill.
        draw.ellipse((0, 0) + self.circle_thumb_size, fill=255)
        # Fit the image to the mask
        circle_thumbnail = ImageOps.fit(image_obj, mask.size, centering=(0.5, 0.5))
        circle_thumbnail.putalpha(mask)
        circle_thumbnail.save(circle_thumbnail_file_name)

        circle_thumb = Image.open(circle_thumbnail_file_name)

        return circle_thumb


    def create_normal_thumbnail(self, file_name, thumbnail_base_width):

        basewidth = thumbnail_base_width
        img = Image.open(file_name).convert("RGBA")

        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth,hsize), Image.ANTIALIAS)

        return img


if __name__ == "__main__":

    cards = SocialMediaImageAutomation("updates.csv", ["HKG18-Social-Media-bg.jpg"])
