from app import cel, create_app

app = create_app()
app.app_context().push()