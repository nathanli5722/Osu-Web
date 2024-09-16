from flask import render_template, Flask, request, make_response, redirect, send_file
from zipfile import BadZipFile, ZipFile
from threading import Thread

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')




@app.route("/play", methods=['GET', 'POST'])
def play():
    if request.method == 'POST':
        beatmap = request.files.get('beatmap')
        #os.rename(beatmap.filename, "beatmap.zip")
        skin = request.files.get('skin')

        try:
            with ZipFile(beatmap, 'r') as beatmap_ref:
                beatmap_ref.extractall("static/beatmaps/" + beatmap.filename)


            with ZipFile(skin, 'r') as skin_ref:
                skin_ref.extractall("static/skins/" + skin.filename)

        except BadZipFile:
            print("ZIPPED BAD")
            return render_template("error.html", error='Error with unzipping files')
        
        return set_cookie(beatmap, skin)
    else:
        return render_template('play.html', beatmap=request.cookies.get('beatmap'), skin=request.cookies.get('skin'))
    
def set_cookie(beatmap, skin):
    print('making cookies')
    resp = make_response(redirect("/play"))
    resp.set_cookie("beatmap", "beatmaps/" + beatmap.filename)
    resp.set_cookie("skin", "skins/" + skin.filename)
    return resp



#use to get image, but im not sure lol
@app.post("/get")
def get():
    url = request.args.get(default="0")

    if url == "0":
        return render_template('error.html', 500)
    
    return send_file("static/skin/" + url, mimetype="image/png")



if __name__ == "__main__":
    app.run(port=8001)