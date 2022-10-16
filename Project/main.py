
from logging import debug
from website import create_app


app=create_app()



if __name__=='__main__':
    app.run(debug=True) 
#it runs the web server if we run the file      
