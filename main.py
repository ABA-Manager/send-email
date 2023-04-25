from fastapi_mail import FastMail, ConnectionConfig, MessageSchema
from fastapi import FastAPI, HTTPException
import os

import Setting
from Models.models import Database


#load_dotenv()

app = FastAPI()

# Configuración de la conexión SMTP
conf = ConnectionConfig(

    MAIL_USERNAME=Setting.MAIL_USERNAME,
    MAIL_PASSWORD=Setting.MAIL_PASSWORD,
    MAIL_FROM=Setting.MAIL_FROM,
    MAIL_PORT=Setting.MAIL_PORT,
    MAIL_SERVER=Setting.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)


@app.post("/send_email/{contractor_id}")
async def send_email(contractor_id: int):
    fm = FastMail(conf)

    db = Database(

       Setting.DB_HOST,
       Setting.DB_NAME,
       Setting.DB_USER,
       Setting.DB_PASSWORD
    )
    name, email = db.get_contractor_email(contractor_id)
    #Cambiar con la direccion del servidor
    link = f"{Setting.URL_COMPANY}/register/{contractor_id}"

    with open("/app/Templates/email_template.html", "r",encoding='utf-8') as f:
        template = f.read()

    body = template.replace('{{ name }}', name).replace('{{ link }}',link )

    # Creamos el mensaje
    message = MessageSchema(
        subject="Clinic App Notification",
        recipients=[email],
        body=body,
        subtype="html"
    )

    try:
        await fm.send_message(message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "El correo electr\u00f3nico ha sido enviado exitosamente"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
