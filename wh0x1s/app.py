from flask import Flask,render_template,request,send_from_directory
import whois
import os
import validators

app = Flask(__name__)

def make_dir():
    if not os.path.exists("files"):
        os.makedirs("files")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result',methods=['POST'])
def result():
    if request.method == "POST":
        web = request.form.get('website').strip()
        if not validators.domain(web):
            msg = "Invalid domain! Please enter a correct domain name (e.g., example.com)."
            return render_template('message.html',msg=msg)
        try:
            data = whois.whois(web)
    
            whois_data = {
                        "domain_name": data.domain_name,
                        "registrar": data.registrar,
                        "registrar_url": data.registrar_url,
                        "reseller": data.reseller,
                        "whois_server": data.whois_server,
                        "referral_url": data.referral_url,
                        "updated_date": data.updated_date,
                        "creation_date": data.creation_date,
                        "expiration_date": data.expiration_date,
                        "name_servers": data.name_servers,
                        "status": data.status,
                        "emails": data.emails,
                        "dnssec": data.dnssec,
                        "name": data.name,
                        "org": data.org,
                        "address": data.address,
                        "city": data.city,
                        "state": data.state,
                        "registrant_postal_code": data.registrant_postal_code,
                        "country": data.country
            }

            file_path = os.path.join("files", "whois_data.txt")
            with open(file_path,'w',encoding="utf-8") as f:
                f.write(str(data))
            return render_template('result.html',data=whois_data)
        
        except Exception as e:
            msg = "An error occurred while fetching WHOIS data. Please check the domain and try again."

            return render_template('message.html',msg=msg)
    return render_template('index.html')

@app.route("/download")
def download_file():
    return send_from_directory("files","whois_data.txt", as_attachment=True)


if __name__ == "__main__":
    make_dir()
    app.run(debug=True)