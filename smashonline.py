import web
from web import form
import model
from captcha import getCaptcha

# List of valid time zones
olsonDB = [
    'Pacific/Majuro',
    'Pacific/Pago_Pago',
    'America/Adak',
    'Pacific/Honolulu',
    'Pacific/Marquesas',
    'Pacific/Gambier',
    'America/Anchorage',
    'America/Los_Angeles',
    'Pacific/Pitcairn',
    'America/Phoenix',
    'America/Denver',
    'America/Guatemala',
    'America/Chicago',
    'Pacific/Easter',
    'America/Bogota',
    'America/New_York',
    'America/Caracas',
    'America/Halifax',
    'America/Santo_Domingo',
    'America/Santiago',
    'America/St_Johns',
    'America/Godthab',
    'America/Argentina/Buenos_Aires',
    'America/Montevideo',
    'America/Noronha',
    'America/Noronha',
    'Atlantic/Azores',
    'Atlantic/Cape_Verde',
    'UTC',
    'Europe/London',
    'Europe/Berlin',
    'Africa/Lagos',
    'Africa/Windhoek',
    'Asia/Beirut',
    'Africa/Johannesburg',
    'Asia/Baghdad',
    'Europe/Moscow',
    'Asia/Tehran',
    'Asia/Dubai',
    'Asia/Baku',
    'Asia/Kabul',
    'Asia/Yekaterinburg',
    'Asia/Karachi',
    'Asia/Kolkata',
    'Asia/Kathmandu',
    'Asia/Dhaka',
    'Asia/Omsk',
    'Asia/Rangoon',
    'Asia/Krasnoyarsk',
    'Asia/Jakarta',
    'Asia/Shanghai',
    'Asia/Irkutsk',
    'Australia/Eucla',
    'Australia/Eucla',
    'Asia/Yakutsk',
    'Asia/Tokyo',
    'Australia/Darwin',
    'Australia/Adelaide',
    'Australia/Brisbane',
    'Asia/Vladivostok',
    'Australia/Sydney',
    'Australia/Lord_Howe',
    'Asia/Kamchatka',
    'Pacific/Noumea',
    'Pacific/Norfolk',
    'Pacific/Auckland',
    'Pacific/Tarawa',
    'Pacific/Chatham',
    'Pacific/Tongatapu',
    'Pacific/Apia',
    'Pacific/Kiritimati'
]

render = web.template.render('templates/')

urls = (
    '/', 'index',
    '/create', 'create_match',
    '/captcha.gif', 'captcha',
)

# Some session code for the captcha
app = web.application(urls, locals())
if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'captcha': ''})
    web.config._session = session
else:
    session = web.config._session
    
matchForm = form.Form(
    form.Textbox('title', form.notnull, description="Match Title"),
    form.Textbox('net_code', form.notnull, description="Net Code"),
    form.Password('password', description="Password", post="<span> Optional</span>"),
    form.Textbox('captcha', form.notnull, description="Validation Code", pre="<img src='/captcha.gif' valign=center><br>", style="width:70px;"),
    form.Hidden('timezone', form.notnull, value="America/New_York"),
    form.Button('Create Game'),
    validators = [
        form.Validator("Invalid net code", lambda i: len(i.net_code) == 8 ),   # Check to make sure the netcode is legit
        form.Validator("Title too long", lambda i: len(i.title) <= 25), # Check to make sure the title is within 25 characters
        form.Validator("Invalid password", lambda i: len(i.password) <=25),  # Check to make sure the password isn't too long
        form.Validator("Title is required", lambda i: len(i.title) != 0),   # Check to make sure a title was entered
        form.Validator("You shouldn't see this error", lambda i:  i.timezone in olsonDB),   # Check to make sure the time zone is valid
        form.Validator("Incorrect CAPTCHA", lambda i: i.captcha == session.captcha),]    # Check the CAPTCHA they entered against the one in the session variable
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
            # form.d.boe and form['boe'].value are both ways to extract data
            model.newMatch(title=form.d.title, net_code=form.d.net_code, password=form.d.password, timezone=form.d.timezone)
            raise web.seeother('/')   # Send em to the home page
            
class captcha:
    # Display the captcha
    def GET(self):
        web.header("Content-Type", "image/gif")
        captcha = getCaptcha()
        session.captcha = captcha[0]
        return captcha[1].read()

if __name__ == "__main__":
    app.run()