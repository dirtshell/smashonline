import web
from web import form
import model

render = web.template.render('templates/')

urls = (
    '/', 'index',
    '/create', 'create_match'
)

matchForm = form.Form(
    form.Textbox('title', form.notnull, description="Match Title"),
    form.Textbox('net_code', form.notnull, description="Net Code"),
    form.Button('Create Game'),
    validators = [
        form.Validator("Invalid net code", lambda i: len(i.net_code) == 8 ),   # Check to make sure the netcode is legit
        form.Validator("Title too long", lambda i: len(i.title) <= 25), # Check to make sure the title is within 25 characters
        form.Validator("Title is required", lambda i: len(i.title) != 0),]   # Check to make sure a title was entered 
    )

class index:
    # Display the index page
    def GET(self):
        matches = model.getMatches()    # Get a list of the matches and store them in matches var
        return render.index(matches)

class create_match:
    # Display the create match page
    def GET(self):
        form = matchForm()
        return render.create(form)
    
    # Save the data    
    def POST(self): 
        form = matchForm() 
        if not form.validates():    # If there is an issue
            return render.create(form)    # Return them to the create page
        else:   # Otherwise save it
            # form.d.boe and form['boe'].value are equivalent ways of
            # extracting the validated arguments from the form.
            model.newMatch(title=form.d.title, net_code=form.d.net_code)
            raise web.seeother('/')   # Send em to the home page

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()