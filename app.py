# from flask import Flask, render_template, request, redirect, url_for
# import os
# import mimetypes
# import google.generativeai as genai
# from dotenv import load_dotenv

# load_dotenv()
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# app = Flask(__name__)

# UPLOAD_FOLDER = "static/uploads"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # Gemini call
# def get_nutrition_info(image_path):
#     with open(image_path, "rb") as img_file:
#         image_data = img_file.read()

#     mime_type, _ = mimetypes.guess_type(image_path)
#     if not mime_type:
#         raise ValueError("Could not determine MIME type of the image.")

#     model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")


#     prompt = (
#         "Analyze this food image and provide a detailed nutrition breakdown "
#         "in a **well-formatted table** including food item names, estimated calories, "
#         "protein, fat, carbohydrates, fiber, and vitamins."
#     )

#     image_blob = {"mime_type": mime_type, "data": image_data}
#     response = model.generate_content([prompt, image_blob])

#     return response.text

# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         if "file" not in request.files:
#             return "No file uploaded", 400

#         file = request.files["file"]
#         if file.filename == "":
#             return "No selected file", 400

#         file_path = os.path.join(UPLOAD_FOLDER, file.filename)
#         file.save(file_path)

#         # Get Gemini nutrition analysis
#         result = get_nutrition_info(file_path)

#         return render_template("index.html", result=result, image_url=file_path)

#     return render_template("index.html")

# if __name__ == "__main__":
#     app.run(debug=True)
from flask import Flask, render_template, request
import os
import mimetypes
import google.generativeai as genai

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_nutrition_info(image_path):
    with open(image_path, "rb") as img_file:
        image_data = img_file.read()

    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type:
        raise ValueError("Could not determine MIME type of the image.")

    model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")

    prompt = (
        "Analyze this food image and provide a detailed nutrition breakdown "
        "in a well-formatted Markdown table with food item, calories, protein, fat, carbs, and fiber."
    )

    image_blob = {"mime_type": mime_type, "data": image_data}
    response = model.generate_content([prompt, image_blob])
    return response.text


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(filepath)

            result = get_nutrition_info(filepath)
            # 👇 pass only filename, not full path
            return render_template("index.html", image_url=filename, result=result)

    return render_template("index.html", image_url=None, result=None)


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
