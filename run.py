from app import app

if __name__ == "__main__":
   app.secret_key = '95cd848d46885101a9ed645d17eecb1ae5c4c0feac17601b5fb890d88bee6a57'
   app.run(debug=True)