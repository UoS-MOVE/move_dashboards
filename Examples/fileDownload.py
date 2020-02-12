@app.server.route('/dash/urlToDownload') 
def download_csv():
    return send_file('output/downloadFile.csv',
                     mimetype='text/csv',
                     attachment_filename='downloadFile.csv',
                     as_attachment=True)