from flask import render_template, Flask, request
from zipfile import ZipFile
import os;

app = Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')




@app.route("/play", methods=['GET', 'POST'])
def play():
    if request.method == 'POST':
        beatmap = request.files.get('beatmap')
        #os.rename(beatmap.filename, "beatmap.zip")

        try:
            with ZipFile(beatmap, 'r') as beatmap_ref:
                beatmap_ref.extractall(beatmap)


            skin = request.files.get('skin')

            with ZipFile(skin, 'r') as skin_ref:
                skin_ref.extractall(skin)

        except BadZipFile:
            return render_template("error.html", error='Error with unzipping files')
        return render_template('play.html', beatmap=beatmap, skin=skin)
    else:
        return render_template('play.html', beatmap=beatmap, skin=skin)